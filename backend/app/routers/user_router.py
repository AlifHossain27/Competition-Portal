import traceback
from typing import Annotated, List
from uuid import UUID
from app.core.config import settings
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.rate_limiting import limiter
from app.db.deps import get_db
from app.schemas.user_schemas import UserCreate, UserUpdate, UserSchema, Token, PasswordChange
from app.services.user_service import (
    register_user,
    login_user,
    get_user_by_uuid,
    change_password,
    update_user,
    logout_user,
    CurrentUser,
    list_users,
    approve_club
)
from app.exceptions.handler import (
    NotFoundException,
    ConflictException,
    EntityTooLargeException,
    BadRequestException,
    UnauthorizedException
)


user_router = APIRouter()

@user_router.post("/auth", response_model=UserSchema, status_code=201)
@limiter.limit("10/minute")
async def register_user_route(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(user=user, db=db)
    except (NotFoundException, ConflictException, BadRequestException, UnauthorizedException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.post("/auth/token", response_model=Token)
@limiter.limit("10/minute")
async def login_route(request: Request, response: Response, data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    try:
        token = login_user(data=data, db=db)
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            path="/",
        )
        return token
    except (NotFoundException, ConflictException, BadRequestException, UnauthorizedException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.post("/auth/logout", status_code=204)
async def logout_route(response: Response):
    try:
        logout_user(response)
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.get("/users", response_model=List[UserSchema])
def get_all_users(current_user: CurrentUser, db: Session = Depends(get_db)):
    try:
        return list_users(current_user=current_user, db=db)
    except (NotFoundException, ConflictException, BadRequestException, UnauthorizedException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.get("/user/me", response_model=UserSchema)
async def get_current_user_route(current_user: CurrentUser, db: Session = Depends(get_db)):
    try:
        return get_user_by_uuid(uuid=current_user.get_id(), db=db)
    except (NotFoundException, ConflictException, BadRequestException, UnauthorizedException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.patch("/user/me", response_model=UserSchema, status_code=201)
async def update_user_route(current_user: CurrentUser, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        uuid = current_user.get_id()
        return update_user(current_user=current_user, uuid=uuid, updated_attributes=user, db=db)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.get("/user/{user_id}", response_model=UserSchema, status_code=200)
def admin_get_user(current_user: CurrentUser, user_id: UUID, db: Session = Depends(get_db)):
    try:
        user = get_user_by_uuid(uuid=current_user.get_id(), db=db)
        if user.role == "admin":
            return get_user_by_uuid(user_id, db)
    except (NotFoundException, UnauthorizedException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.patch("/user/{user_id}", response_model=UserSchema, status_code=201)
async def update_user_route(current_user: CurrentUser, user_id:UUID, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        return update_user(current_user=current_user, uuid=user_id, updated_attributes=user, db=db)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    

    
@user_router.patch("/user/change-password", status_code=200)
async def change_password_route(new_password: PasswordChange, current_user: CurrentUser, db: Session = Depends(get_db)):
    try:
        change_password(current_user=current_user, new_password=new_password, db=db)
        return {"detail": "Password changed successfully"}
    except (NotFoundException, ConflictException, BadRequestException, UnauthorizedException) as error:
        raise error
    except Exception:
        print(traceback.format_exc())
        raise BadRequestException()
    
@user_router.post("/clubs/{club_id}/approve")
def approve_club_by_admin(club_id: int, status: str, current_user: CurrentUser, db: Session = Depends(get_db)):
    club = approve_club(current_user=current_user,db=db, club_id=club_id, status=status)
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    return {"message": f"Club {club.name} {status} successfully"}