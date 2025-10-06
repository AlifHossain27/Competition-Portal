from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import List
from app.schemas.event_schemas import EventSchema

class ClubStatusEnum(str, Enum):
    pending = "pending"
    active = "active"
    rejected = "rejected"

class ClubBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    logo_url: str| None = None
    banner_url: str | None = None
    website: str | None = None
    

class ClubCreate(ClubBase):
    pass

class ClubSchema(ClubBase):
    id: UUID
    status: ClubStatusEnum = ClubStatusEnum.pending
    created_by: UUID
    approved_by: UUID | None = None
    created_at: datetime
    updated_at: datetime
    events: List[EventSchema] = []

    model_config = ConfigDict(from_attributes=True)
