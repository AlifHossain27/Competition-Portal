from sqlalchemy import Column, String, ForeignKey, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db.database import Base

class RegistrationStatusEnum(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class PaymentStatusEnum(str, enum.Enum):
    unpaid = "unpaid"
    paid = "paid"
    refunded = "refunded"

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"))
    form_response_id = Column(UUID(as_uuid=True), ForeignKey("form_responses.id"))
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    status = Column(Enum(RegistrationStatusEnum), default=RegistrationStatusEnum.pending)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    ticket_code = Column(String, nullable=True)
    payment_status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.unpaid)

    event = relationship("Event", back_populates="registrations")
    form_response = relationship("FormResponse", back_populates="registration")
    team = relationship("Team", back_populates="registrations")
