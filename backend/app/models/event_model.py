from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.db.database import Base

class EventStatusEnum(str, enum.Enum):
    draft = "draft"
    published = "published"
    closed = "closed"
    cancelled = "cancelled"

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    club_id = Column(UUID(as_uuid=True), ForeignKey("clubs.id"))
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    poster_url = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    registration_deadline = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    max_participants = Column(Integer, nullable=True)
    status = Column(Enum(EventStatusEnum), default=EventStatusEnum.draft, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    club = relationship("Club", back_populates="events")
    forms = relationship("Form", back_populates="event")
    registrations = relationship("Registration", back_populates="event")
    teams = relationship("Team", back_populates="event")
