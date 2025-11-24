from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum
from app.schemas.club_schemas import ClubSchema

class UserRoleEnum(str, Enum):
    admin = "admin"
    regular = "regular"
    club = "club"



class UserBase(BaseModel):
    email: EmailStr
    name: str
    university_id: str | None = None



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    university_id: str | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    university_id: str | None = None
    role: UserRoleEnum | str | None = None


class UserSchema(UserBase):
    id: UUID
    role: UserRoleEnum | str
    created_at: datetime
    updated_at: datetime
    club: ClubSchema | None = None
    model_config = ConfigDict(from_attributes=True)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: UUID | None = None

    def get_id(self) -> UUID | None:
        if self.id:
            return self.id
        return None
