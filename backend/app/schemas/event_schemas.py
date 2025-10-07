from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import List
from app.schemas.form_schemas import FormSchema, FormResponseModelSchema
from app.schemas.registration_schemas import RegistrationSchema
from app.schemas.team_schemas import TeamSchema

class EventStatusEnum(str, Enum):
    draft = "draft"
    published = "published"
    closed = "closed"
    cancelled = "cancelled"

class EventBase(BaseModel):
    title: str
    slug: str
    type: str | None = None
    description: str | None = None
    poster_url: str | None = None
    start_time: datetime
    end_time: datetime
    registration_deadline: datetime | None = None
    location: str | None = None
    max_participants: int | None = None
    

class EventCreate(EventBase):
    pass

class EventSchema(EventBase):
    id: UUID
    club_id: UUID
    created_at: datetime
    updated_at: datetime
    status: EventStatusEnum = EventStatusEnum.draft
    forms: List[FormSchema] = []

    model_config = ConfigDict(from_attributes=True)

class EventModelSchema(EventBase):
    id: UUID
    club_id: UUID
    created_at: datetime
    updated_at: datetime
    status: EventStatusEnum = EventStatusEnum.draft
    forms: List[FormResponseModelSchema] = []
    registrations: List[RegistrationSchema] = []
    teams: List[TeamSchema] = []

    model_config = ConfigDict(from_attributes=True)
