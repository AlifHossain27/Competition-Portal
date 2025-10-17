from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.form_schemas import FormResponseCreate, FormResponseSchema
from app.schemas.registration_schemas import RegistrationFullSchema, RegistrationSchema, PaymentStatusEnum
from app.schemas.user_schemas import TokenData
from app.services.registration_service import (
    get_all_registrations,
    get_registration,
    get_registration_stats,
    update_payment_status,
    confirm_registration,
    cancel_registration
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

registration_router = APIRouter()

@registration_router.get("/club/{club_id}/event/{event_id}/registrations", response_model=list[RegistrationSchema], status_code=200)
async def fetch_all_registrations_router(club_id: UUID, event_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return get_all_registrations(current_user=current_user, db=db, club_id=club_id, event_id=event_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@registration_router.get("/club/{club_id}/event/{event_id}/registrations/{registration_id}", response_model=RegistrationFullSchema, status_code=200)
async def fetch_registration_router(club_id: UUID, event_id: UUID, registration_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return get_registration(current_user=current_user, db=db, club_id=club_id, event_id=event_id,registration_id=registration_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@registration_router.patch("/club/{club_id}/event/{event_id}/registrations/{registration_id}/confirm", response_model=RegistrationSchema, status_code=201)
async def confirm_registration_router(club_id: UUID, event_id: UUID, registration_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return confirm_registration(current_user=current_user, db=db, club_id=club_id, event_id=event_id, registration_id=registration_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@registration_router.patch("/club/{club_id}/event/{event_id}/registrations/{registration_id}/cancel", response_model=RegistrationSchema, status_code=201)
async def cancel_registration_router(club_id: UUID, event_id: UUID, registration_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return cancel_registration(current_user=current_user, db=db, club_id=club_id, event_id=event_id, registration_id=registration_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@registration_router.patch("/club/{club_id}/event/{event_id}/registrations/{registration_id}/payment/{payment_status}", response_model=RegistrationSchema, status_code=201)
async def update_registration_payment_router(club_id: UUID, event_id: UUID, registration_id: UUID, payment_status: str,db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return update_payment_status(current_user=current_user, db=db, club_id=club_id, event_id=event_id, registration_id=registration_id, payment_status=payment_status)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e
    
@registration_router.get("/club/{club_id}/event/{event_id}/registrations/stats", status_code=200)
async def registration_statistics_router(club_id: UUID, event_id: UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    try:
        return get_registration_stats(current_user, db, club_id, event_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e