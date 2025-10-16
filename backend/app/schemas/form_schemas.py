from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import List
from app.schemas.team_schemas import TeamMemberCreate

class FormResponseBase(BaseModel):
    response_content: str

class FormResponseCreate(FormResponseBase):
    team_name: str
    leader_name: str
    leader_email: EmailStr
    members: List[TeamMemberCreate]

class FormResponseSchema(FormResponseBase):
    id: UUID
    form_id: UUID
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FormStatusEnum(str, Enum):
    draft = "draft"
    published = "published"
    closed = "closed"


class FormBase(BaseModel):
    title: str
    instructions: str | None = None
    form_content: str | None = None

class FormCreate(FormBase):
    pass

class FormSchema(FormBase):
    id: UUID
    event_id: UUID
    status: FormStatusEnum = FormStatusEnum.draft
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FormResponseModelSchema(FormBase):
    id: UUID
    event_id: UUID
    status: FormStatusEnum = FormStatusEnum.draft
    created_at: datetime
    updated_at: datetime
    responses: List[FormResponseSchema] = []

    model_config = ConfigDict(from_attributes=True)

    