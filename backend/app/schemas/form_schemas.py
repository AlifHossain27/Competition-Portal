from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List

class FormResponseBase(BaseModel):
    response_content: str

class FormResponseCreate(FormResponseBase):
    form_id: UUID

class FormResponseSchema(FormResponseBase):
    id: UUID
    form_id: UUID
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FormBase(BaseModel):
    title: str
    instructions: str | None = None
    form_content: str | None = None

class FormCreate(FormBase):
    event_id: UUID

class FormSchema(FormBase):
    id: UUID
    event_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FormResponseModelSchema(FormBase):
    id: UUID
    event_id: UUID
    created_at: datetime
    updated_at: datetime
    responses: List[FormResponseSchema] = []

    model_config = ConfigDict(from_attributes=True)

    