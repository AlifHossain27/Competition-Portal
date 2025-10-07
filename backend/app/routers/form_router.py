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
from app.exceptions.handler import (
    NotFoundException,
    ConflictException,
    EntityTooLargeException,
    BadRequestException,
    UnauthorizedException
)

form_router = APIRouter()

@form_router.post("/club/{club_id}/event/{event_id}/form/create", response_model=FormSchema, status_code=201)
def create_new_form( club_id: UUID, event_id: UUID, form_data: FormCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return create_form(current_user, db, form_data, event_id, club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{club_id}/event/{event_id}/form/all", response_model=list[FormSchema], status_code=200)
async def list_all_forms(club_id: UUID, event_id: UUID, skip: int = 0, limit: int = None, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return get_all_forms(db, current_user, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{club_id}/event/{event_id}/form/published", response_model=list[FormSchema], status_code=200)
async def list_published_forms(club_id: UUID, event_id: UUID, skip: int = 0, limit: int = None,db: Session = Depends(get_db)):
    try:
        return get_published_forms(db, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{club_id}/event/{event_id}/form/draft", response_model=list[FormSchema], status_code=200)
async def list_draft_forms(club_id: UUID,event_id: UUID, skip: int = 0, limit: int = None, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return get_draft_forms(db, current_user, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{club_id}/event/{event_id}/form/closed", response_model=list[FormSchema], status_code=200)
async def list_closed_forms(club_id: UUID, event_id: UUID, skip: int = 0, limit: int = None, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return get_closed_forms(db, current_user, event_id, club_id, skip, limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.get("/club/{club_id}/event/{event_id}/form/{form_id}", response_model=FormSchema, status_code=200)
async def read_form(club_id: UUID, event_id: UUID, form_id: UUID, db: Session = Depends(get_db)):
    try:
        return get_form(db, form_id, event_id, club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{club_id}/event/{event_id}/form/{form_id}", response_model=FormSchema, status_code=201)
async def update_existing_form(club_id: UUID, event_id: UUID, form_id: UUID, form_data: FormCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return update_form(db, current_user, club_id, event_id, form_id, form_data)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.delete("/club/{club_id}/event/{event_id}/form/{form_id}", response_model=FormSchema, status_code=204)
async def remove_form(club_id: UUID, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return delete_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{club_id}/event/{event_id}/form/{form_id}/publish", response_model=FormSchema, status_code=201)
async def publish_existing_form(club_id: UUID, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return publish_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{club_id}/event/{event_id}/form/{form_id}/draft", response_model=FormSchema, status_code=201)
async def mark_form_as_draft(club_id: UUID, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return draft_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@form_router.patch("/club/{club_id}/event/{event_id}/form/{form_id}/close", response_model=FormSchema, status_code=201)
async def mark_form_as_closed(club_id: UUID, event_id: UUID, form_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return close_form(db, current_user, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e