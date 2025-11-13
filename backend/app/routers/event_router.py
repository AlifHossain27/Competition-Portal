import traceback
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.deps import get_db
from app.schemas.event_schemas import EventCreate, EventSchema, EventModelSchema
from app.schemas.user_schemas import TokenData
from app.services import event_service
from app.services.user_service import get_current_user
from app.services.club_service import get_club_by_slug
from app.exceptions.handler import (
    NotFoundException,
    ConflictException,
    EntityTooLargeException,
    BadRequestException,
    UnauthorizedException
)

event_router = APIRouter()


@event_router.post("/club/{slug}/event/create", response_model=EventSchema, status_code=201)
async def create_event_router(slug: str, data: EventCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.create_event(current_user, db, data, club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.get("/club/{club_id}/event/published", response_model=List[EventSchema], status_code=200)
async def get_published_events_by_club_router(club_id: UUID, skip: int = 0, limit: int = None, db: Session = Depends(get_db)):
    try:
        return event_service.get_published_events_by_club(club_id, db, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.get("/club/{slug}/event/all", response_model=List[EventModelSchema], status_code=200)
async def get_all_events_by_club_router(slug: str, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user), skip: int = 0, limit: int = None):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.get_all_events_by_club(current_user, club_id, db, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.get("/club/{slug}/event/draft", response_model=List[EventModelSchema], status_code=200)
async def get_draft_events_by_club_router(slug: str, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user), skip: int = 0, limit: int = None):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.get_draft_events_by_club(current_user, club_id, db, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.get("/club/{slug}/event/closed", response_model=List[EventModelSchema], status_code=200)
async def get_closed_events_by_club_router(slug: str, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user), skip: int = 0, limit: int = None):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.get_closed_events_by_club(current_user, club_id, db, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.get("/club/{slug}/event/cancelled", response_model=List[EventModelSchema], status_code=200)
async def get_cancelled_events_by_club_router(slug: str, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user), skip: int = 0, limit: int = None):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.get_cancelled_events_by_club(current_user, club_id, db, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.get("/club/{slug}/event/{event_id}", response_model=EventSchema, status_code=200)
async def get_event_router(slug: str, event_id: UUID, db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.get_event(db, club_id, event_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@event_router.patch("/club/{slug}/event/{event_id}", response_model=EventSchema, status_code=201)
async def update_event_router(slug, event_id: UUID, data: EventCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.update_event(current_user, db, club_id, event_id, data)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.delete("/club/{slug}/event/{event_id}", status_code=204)
async def delete_event_router(slug: str, event_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.delete_event(current_user, db, club_id, event_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e


@event_router.patch("/club/{slug}/event/{event_id}/publish", response_model=EventModelSchema, status_code=201)
async def publish_event_router(slug: str, event_id: UUID,db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.publish_event(current_user, club_id, event_id, db)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.patch("/club/{slug}/event/{event_id}/close", response_model=EventModelSchema, status_code=201)
async def close_event_router(slug: str, event_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.close_event(current_user, club_id, event_id, db)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@event_router.patch("/club/{slug}/event/{event_id}/cancel", response_model=EventModelSchema, status_code=201)
async def cancel_event_router(slug: str, event_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return event_service.cancel_event(current_user, club_id, event_id, db)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
