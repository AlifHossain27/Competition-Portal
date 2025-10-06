from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum

class RegistrationStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class PaymentStatusEnum(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    refunded = "refunded"

class RegistrationBase(BaseModel):
    status: RegistrationStatusEnum = RegistrationStatusEnum.pending
    ticket_code: str | None = None
    payment_status: PaymentStatusEnum = PaymentStatusEnum.unpaid

class RegistrationCreate(RegistrationBase):
    event_id: UUID
    form_response_id: UUID
    team_id: UUID

class RegistrationSchema(RegistrationBase):
    id: UUID
    event_id: UUID
    form_response_id: UUID
    team_id: UUID
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)
