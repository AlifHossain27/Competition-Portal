from pydantic import BaseModel, HttpUrl, ConfigDict
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
    logo_url: HttpUrl | None = None
    banner_url: HttpUrl | None = None
    website: HttpUrl | None = None
    status: ClubStatusEnum = ClubStatusEnum.pending

class ClubCreate(ClubBase):
    created_by: UUID

class ClubResponse(ClubBase):
    id: UUID
    created_by: UUID
    approved_by: UUID | None = None
    created_at: datetime
    updated_at: datetime
    events: List[EventSchema] = []

    model_config = ConfigDict(from_attributes=True)
