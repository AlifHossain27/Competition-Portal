from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List

class TeamMemberBase(BaseModel):
    member_name: str
    member_email: EmailStr
    member_student_id: str | None = None

class TeamMemberCreate(TeamMemberBase):
    team_id: UUID | None = None

class TeamMemberSchema(TeamMemberBase):
    id: UUID
    team_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamBase(BaseModel):
    team_name: str
    leader_name: str
    leader_email: EmailStr

class TeamCreate(TeamBase):
    event_id: UUID

class TeamSchema(TeamBase):
    id: UUID
    event_id: UUID
    created_at: datetime
    updated_at: datetime
    members: List[TeamMemberSchema] = []

    model_config = ConfigDict(from_attributes=True)
