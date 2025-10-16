from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from app.models.user_model import User, UserRoleEnum
from app.models.club_model import Club, ClubStatusEnum
from app.models.event_model import Event, EventStatusEnum
from app.models.form_model import Form
from app.schemas.form_schemas import FormCreate, FormSchema, FormStatusEnum
from app.schemas.user_schemas import TokenData
from app.exceptions.handler import (
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
    ConflictException,
    ForbiddenException
)

def create_form(current_user: TokenData, db: Session, form_data: FormCreate, event_id: UUID, club_id: UUID) -> FormSchema:
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    form = Form(
        title = form_data.title,
        instructions = form_data.instructions,
        form_content = form_data.form_content,
        event_id = event.id,
        status = FormStatusEnum.draft
    )
    db.add(form)
    db.commit()
    db.refresh(form)
    return form

def get_form(db: Session, form_id: UUID, event_id: UUID, club_id: UUID):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    
    return db.query(Form).filter(Form.id == form_id).first()

def get_published_forms(db: Session, event_id: UUID, club_id: UUID, skip: int = 0, limit: int = None):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    
    return db.query(Form).filter(Form.event_id == event.id).filter(Form.status == FormStatusEnum.published).offset(skip).limit(limit).all()

def get_draft_forms(db: Session, current_user: TokenData, event_id: UUID, club_id: UUID, skip: int = 0, limit: int = None):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    return db.query(Form).filter(Form.event_id == event.id).filter(Form.status == FormStatusEnum.draft).offset(skip).limit(limit).all()

def get_closed_forms(db: Session, current_user: TokenData, event_id: UUID, club_id: UUID, skip: int = 0, limit: int = None):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    return db.query(Form).filter(Form.event_id == event.id).filter(Form.status == FormStatusEnum.closed).offset(skip).limit(limit).all()

def get_all_forms(db: Session, current_user: TokenData, event_id: UUID, club_id: UUID, skip: int = 0, limit: int = None):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    return db.query(Form).filter(Form.event_id == event.id).offset(skip).limit(limit).all()

def update_form(db: Session, current_user: TokenData, club_id: UUID, event_id: UUID, form_id: UUID, form_data: FormCreate):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise ForbiddenException("You are not authorized to modify this form.")

    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise NotFoundException(f"Form with id {form_id} not found")
    
    form.title = form_data.title
    form.instructions = form_data.instructions
    form.form_content = form_data.form_content
    form.updated_at = datetime.now(tz = timezone.utc)

    db.commit()
    db.refresh(form)
    return form

def delete_form(db: Session, current_user: TokenData, club_id: UUID, event_id: UUID, form_id: UUID):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise ForbiddenException("You are not authorized to modify this form.")

    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise NotFoundException(f"Form with id {form_id} not found")
    
    db.delete(form)
    db.commit()
    return form

def publish_form(db: Session, current_user: TokenData, club_id: UUID, event_id: UUID, form_id: UUID):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise ForbiddenException("You are not authorized to modify this form.")

    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise NotFoundException(f"Form with id {form_id} not found")
    
    form.status = FormStatusEnum.published
    db.commit()
    db.refresh(form)
    return form

def draft_form(db: Session, current_user: TokenData, club_id: UUID, event_id: UUID, form_id: UUID):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise ForbiddenException("You are not authorized to modify this form.")

    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise NotFoundException(f"Form with id {form_id} not found")
    
    form.status = FormStatusEnum.draft
    db.commit()
    db.refresh(form)
    return form

def close_form(db: Session, current_user: TokenData, club_id: UUID, event_id: UUID, form_id: UUID):
    club = db.query(Club).filter(Club.id == club_id).first()
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NotFoundException(f"Event with id {event_id} not found")
    if event.club_id != club.id:
        raise NotFoundException(f"Event with id {event_id} not found in club with id {club_id}")
    if club.created_by != current_user.get_id():
        raise ForbiddenException("You are not authorized to modify this form.")

    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise NotFoundException(f"Form with id {form_id} not found")
    
    form.status = FormStatusEnum.closed
    db.commit()
    db.refresh(form)
    return form

