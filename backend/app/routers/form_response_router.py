from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.form_schemas import FormResponseCreate, FormResponseSchema
from app.schemas.registration_schemas import RegistrationFullSchema
from app.schemas.user_schemas import TokenData
from app.services.form_response_service import (
    create_form_response,
    list_form_responses,
    get_form_response
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

form_response_router = APIRouter()

@form_response_router.post("/club/{club_id}/event/{event_id}/form/{form_id}/form-response/create", response_model=RegistrationFullSchema, status_code=201)
async def create_new_form_response_router( form_id: UUID, club_id: UUID, event_id: UUID, response_data: FormResponseCreate, db: Session = Depends(get_db)):
    try:
        return create_form_response(db, response_data, form_id, event_id, club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@form_response_router.get("/club/{club_id}/event/{event_id}/form/{form_id}/form-response", response_model=list[FormResponseSchema], status_code=200)
async def list_form_responses_router( form_id: UUID, club_id: UUID, event_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return list_form_responses(current_user, db, club_id, event_id, form_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@form_response_router.get("/club/{club_id}/event/{event_id}/form/{form_id}/form-response/{response_id}", response_model=list[FormResponseSchema], status_code=200)
async def get_form_responses_router( response_id: UUID, form_id: UUID, club_id: UUID, event_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return get_form_response(current_user, db, club_id, event_id, form_id, response_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e