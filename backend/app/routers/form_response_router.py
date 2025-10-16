from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.form_schemas import FormResponseCreate, FormResponseSchema
from app.schemas.registration_schemas import RegistrationSchema
from app.schemas.user_schemas import TokenData
from app.services.form_response_service import (
    create_form_response
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

@form_response_router.post("/club/{club_id}/event/{event_id}/form/{form_id}/formresponse/create", response_model=RegistrationSchema, status_code=201)
def create_new_form_response( form_id: UUID, club_id: UUID, event_id: UUID, response_data: FormResponseCreate, db: Session = Depends(get_db)):
    try:
        return create_form_response(db, response_data, form_id, event_id, club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e