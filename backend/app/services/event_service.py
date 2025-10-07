from typing import List
from uuid import UUID
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.event_model import Event, EventStatusEnum
from app.models.club_model import Club, ClubStatusEnum
from app.models.user_model import User, UserRoleEnum
from app.schemas.event_schemas import EventCreate, EventSchema, EventModelSchema
from app.schemas.user_schemas import TokenData
from app.services.user_service import (
    get_user_by_uuid,
    CurrentUser
)
from app.exceptions.handler import (
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
    ConflictException,
    ForbiddenException
)

def create_event(current_user: TokenData, db: Session, data: EventCreate, club_id: UUID) -> EventSchema:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException("You are not the owner of the Club")
    event = Event(
        club_id = club_id,
        title = data.title,
        slug = data.slug,
        type = data.type,
        description = data.description,
        poster_url = data.poster_url,
        start_time = data.start_time,
        end_time = data.end_time,
        registration_deadline = data.registration_deadline,
        location = data.location,
        max_participants = data.max_participants,
        status = EventStatusEnum.draft
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_published_events(db: Session, skip: int = 0, limit: int = None) -> List[EventSchema]:
    return db.query(Event).filter(Event.status == EventStatusEnum.published).offset(skip).limit(limit).all()


def get_all_events_by_club(current_user: TokenData, club_id: UUID, db: Session, skip: int = 0, limit: int = None) -> List[EventModelSchema]:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    return db.query(Event).filter(Event.club_id == club_id).offset(skip).limit(limit).all()


def get_published_events_by_club(club_id: UUID, db: Session, skip: int = 0, limit: int = None) -> List[EventSchema]:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")

    return db.query(Event).filter(Event.club_id == club_id).filter(Event.status == EventStatusEnum.published).offset(skip).limit(limit).all()


def get_draft_events_by_club(current_user: TokenData, club_id: UUID, db: Session, skip: int = 0, limit: int = None) -> List[EventModelSchema]:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    return db.query(Event).filter(Event.club_id == club_id).filter(Event.status == EventStatusEnum.draft).offset(skip).limit(limit).all()


def get_closed_events_by_club(current_user: TokenData, club_id: UUID, db: Session, skip: int = 0, limit: int = None) -> List[EventModelSchema]:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    return db.query(Event).filter(Event.club_id == club_id).filter(Event.status == EventStatusEnum.closed).offset(skip).limit(limit).all()


def get_cancelled_events_by_club(current_user: TokenData, club_id: UUID, db: Session, skip: int = 0, limit: int = None) -> List[EventModelSchema]:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    return db.query(Event).filter(Event.club_id == club_id).filter(Event.status == EventStatusEnum.cancelled).offset(skip).limit(limit).all()


def get_event(db: Session, club_id: UUID, event_id: UUID) -> EventSchema:
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    return event


def update_event(current_user: TokenData, db: Session, club_id:UUID, event_id: UUID, data: EventCreate) -> EventSchema:
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    
    if club.created_by != current_user.get_id():
        raise ForbiddenException("You can not update this event. You are not the owner of the club.")
    
    event.title = data.title
    event.slug = data.slug
    event.type = data.type
    event.description = data.description
    event.poster_url = data.poster_url
    event.start_time = data.start_time
    event.end_time = data.end_time
    event.registration_deadline = data.registration_deadline
    event.location = data.location
    event.max_participants = data.max_participants
    event.updated_at = datetime.now(tz = timezone.utc)
    
    db.commit()
    db.refresh(event)
    return event


def delete_event(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    
    if club.created_by != current_user.get_id():
        raise ForbiddenException("You can not delete this event. You are not the owner of the club.")

    db.delete(event)
    db.commit()
    return {"detail": "Event deleted successfully"}


def publish_event(current_user: TokenData, club_id:UUID, event_id: UUID, db: Session) -> EventModelSchema:
    user = db.query(User).filter(User.id == current_user.get_id()).first()
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if club.id != event.club_id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != user.id:
        raise UnauthorizedException
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    
    event.status = EventStatusEnum.published
    db.commit()
    db.refresh(event)
    return event


def close_event(current_user: TokenData, club_id:UUID, event_id: UUID, db: Session) -> EventModelSchema:
    user = db.query(User).filter(User.id == current_user.get_id()).first()
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if club.id != event.club_id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != user.id:
        raise UnauthorizedException
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    
    event.status = EventStatusEnum.closed
    db.commit()
    db.refresh(event)
    return event


def cancel_event(current_user: TokenData, club_id:UUID, event_id: UUID, db: Session) -> EventModelSchema:
    user = db.query(User).filter(User.id == current_user.get_id()).first()
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if club.id != event.club_id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != user.id:
        raise UnauthorizedException
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    
    event.status = EventStatusEnum.cancelled
    db.commit()
    db.refresh(event)
    return event

