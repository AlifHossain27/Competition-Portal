from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.form_schemas import FormCreate, FormSchema
from app.schemas.user_schemas import TokenData
from app.services.form_service import (
    create_form,
    get_form,
    get_all_forms,
    get_published_forms,
    get_draft_forms,
    get_closed_forms,
    update_form,
    delete_form,
    publish_form,
    draft_form,
    close_form
)
from app.db.deps import get_db
from app.services.user_service import get_current_user
from app.services.club_service import get_club_by_slug
from app.exceptions.handler import (
    NotFoundException,
    ConflictException,
    EntityTooLargeException,
    BadRequestException,
    UnauthorizedException
)

form_router = APIRouter()

@form_router.post("/club/{slug}/event/{event_id}/form/create", response_model=FormSchema, status_code=201)
async def create_new_form(slug: str, event_id: UUID, form_data: FormCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return create_form(current_user, db, form_data, event_id, club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{slug}/event/{event_id}/form/all", response_model=list[FormSchema], status_code=200)
async def list_all_forms(slug: str, event_id: UUID, skip: int = 0, limit: int = None, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_all_forms(db, current_user, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{slug}/event/{event_id}/form/published", response_model=list[FormSchema], status_code=200)
async def list_published_forms(slug: str, event_id: UUID, skip: int = 0, limit: int = None,db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_published_forms(db, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{slug}/event/{event_id}/form/draft", response_model=list[FormSchema], status_code=200)
async def list_draft_forms(slug: str,event_id: UUID, skip: int = 0, limit: int = None, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_draft_forms(db, current_user, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{slug}/event/{event_id}/form/closed", response_model=list[FormSchema], status_code=200)
async def list_closed_forms(slug: str, event_id: UUID, skip: int = 0, limit: int = None, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_closed_forms(db, current_user, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{slug}/event/{event_id}/form/{form_id}", response_model=FormSchema, status_code=200)
async def read_form(slug: str, event_id: UUID, form_id: UUID, db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_form(db, form_id, event_id, club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{slug}/event/{event_id}/form/{form_id}", response_model=FormSchema, status_code=201)
async def update_existing_form(slug: str, event_id: UUID, form_id: UUID, form_data: FormCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return update_form(db, current_user, club_id, event_id, form_id, form_data)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.delete("/club/{slug}/event/{event_id}/form/{form_id}", status_code=204)
async def remove_form(slug: str, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return delete_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{slug}/event/{event_id}/form/{form_id}/publish", response_model=FormSchema, status_code=201)
async def publish_existing_form(slug: str, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return publish_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{slug}/event/{event_id}/form/{form_id}/draft", response_model=FormSchema, status_code=201)
async def mark_form_as_draft(slug: str, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return draft_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{slug}/event/{event_id}/form/{form_id}/close", response_model=FormSchema, status_code=201)
async def mark_form_as_closed(slug: str, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return close_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e