import traceback
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID, uuid4
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, Cookie,  Response
from app.core.config import settings
from app.models.user_model import User, UserRoleEnum
from app.models.club_model import Club
from app.models.event_model import Event
from app.schemas.user_schemas import Token, TokenData, UserCreate, UserUpdate, UserSchema, PasswordChange
from app.exceptions.handler import (
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
    ConflictException
)


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/auth/token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def authenticate_user(email: str, password: str, db: Session) -> User | Exception:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(plain_password=password, hashed_password=user.password):
        raise UnauthorizedException("Authentication Failed! Wrong email or password")
    return user

def create_access_token(email: str, uuid: UUID, expires_delta: timedelta) -> str:
    payload = {
        'sub': email,
        'id': str(uuid),
        'exp': datetime.now(timezone.utc) + expires_delta
    }

    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

def verify_token(token: str) -> TokenData:
    if not token or token.count('.') != 2:
        raise UnauthorizedException("Invalid token format")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload['id']
        return TokenData(id=user_id)
    except PyJWTError as error:
        print(traceback.format_exc())
        raise UnauthorizedException(error)
    
def get_token_from_cookie(access_token: str | None = Cookie(None)) -> str:
    if not access_token:
        raise UnauthorizedException("Not authenticated")
    return access_token
    
def register_user(db: Session, user: UserCreate) -> UserSchema:
    if db.query(User).filter((User.email == user.email)).first():
        raise ConflictException("User with this email or username already exists")
    new_user = User(
        id = uuid4(),
        name = user.name,
        email = user.email,
        password = get_password_hash(user.password),
        university_id = user.university_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_current_user(token: Annotated[str, Depends(get_token_from_cookie)]) -> TokenData:
    return verify_token(token)

CurrentUser = Annotated[TokenData, Depends(get_current_user)]

def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session) -> Token:
    # Check if there are no users in the DB
    has_user = db.query(User).first()

    # If DB is empty, and login matches ADMIN credentials → auto-register admin
    if not has_user and data.username == settings.ADMIN_EMAIL and data.password == settings.ADMIN_PASSWORD:
        from uuid import uuid4
        admin_user = User(
            id=uuid4(),
            name=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=get_password_hash(settings.ADMIN_PASSWORD),
            role = UserRoleEnum.admin
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        user = admin_user
    else:
        # Normal authentication
        user = authenticate_user(data.username, data.password, db)
        if not user:
            raise UnauthorizedException("Authentication Failed! Wrong email or password")

    # Create JWT token
    token = create_access_token(user.email, user.id, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token, token_type='bearer')


def get_user_by_uuid(uuid: UUID, db: Session) -> User:
    if isinstance(uuid, str):
        try:
            uuid = UUID(uuid)
        except ValueError:
            raise BadRequestException("Invalid UUID")
    user = db.query(User).filter(User.id == uuid).first()
    if not user:
        raise NotFoundException(f"User with ID {uuid} not found")
    return user

def update_user(current_user: TokenData, uuid: UUID, updated_attributes: UserUpdate, db: Session) -> UserSchema:
    user = db.query(User).filter(User.id == uuid).first()
    curr_user = db.query(User).filter(User.id == current_user.get_id()).first()
    if not user:
        raise NotFoundException(f"User with ID {uuid} not found")
    if user.email != updated_attributes.email:
        if db.query(User).filter(User.email == updated_attributes.email).first():
            raise ConflictException(f"User with email {updated_attributes.email} already exists")

    if updated_attributes.email is not None:
        user.email = updated_attributes.email
    if updated_attributes.name is not None:
        user.name = updated_attributes.name
    if updated_attributes.university_id is not None:
        user.university_id = updated_attributes.university_id
    if curr_user.role == UserRoleEnum.admin:
        user.role = updated_attributes.role
    user.updated_at = datetime.now(tz = timezone.utc)

    db.commit()
    db.refresh(user)

    return user

def change_password(current_user: TokenData, new_password: PasswordChange, db: Session) -> None:
    uuid = current_user.get_id()
    user = get_user_by_uuid(uuid=uuid, db=db)

    if new_password.new_password == new_password.current_password:
        raise ConflictException("New password can not be the same as the old password")

    if not verify_password(new_password.current_password, user.password):
        raise UnauthorizedException("Wrong password")
    
    if new_password.new_password != new_password.new_password_confirm:
        raise BadRequestException("New password does not match confirm new password")
    
    user.password = get_password_hash(new_password.new_password)
    db.commit()

def logout_user(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True
    )

# Approve or reject a club
def approve_club(current_user:TokenData, db: Session, club_id: int, status: str):
    uuid = current_user.get_id()
    user = get_user_by_uuid(uuid=uuid, db=db)
    if user.role == UserRoleEnum.admin:
        club = db.query(Club).filter(Club.id == club_id).first()
        if not club:
            return None
        club.status = status  # "approved" or "rejected"
        db.commit()
        db.refresh(club)
        return club
    else:
        raise UnauthorizedException("Admin user required")

# List all users
def list_users(current_user:TokenData, db: Session) -> list[UserSchema]:
    uuid = current_user.get_id()
    user = get_user_by_uuid(uuid=uuid, db=db)
    if user.role == UserRoleEnum.admin:
        return db.query(User).all()
    else:
        raise UnauthorizedException("Admin user required")
