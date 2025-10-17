from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from app.models.user_model import User, UserRoleEnum
from app.models.club_model import Club, ClubStatusEnum
from app.models.event_model import Event, EventStatusEnum
from app.models.form_model import Form, FormResponse
from app.models.team_model import Team, TeamMember
from app.models.registration_model import Registration, RegistrationStatusEnum, PaymentStatusEnum
from app.schemas.form_schemas import FormResponseCreate, FormResponseSchema, FormStatusEnum
from app.schemas.registration_schemas import RegistrationSchema, RegistrationFullSchema
from app.schemas.user_schemas import TokenData
from app.exceptions.handler import (
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
    ConflictException,
    ForbiddenException
)

def get_all_registrations(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID) -> list[RegistrationSchema]:
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club_id).first()
    if not event:
        raise NotFoundException("Event not found or not part of this club")

    club = db.query(Club).filter(Club.id == club_id).first()
    if club.created_by != current_user.get_id():
        raise UnauthorizedException
    
    registrations = db.query(Registration).filter(Registration.event_id == event_id).all()
    return registrations

def get_registration(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, registration_id: UUID) -> RegistrationFullSchema:
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club_id).first()
    if not event:
        raise NotFoundException("Event not found or not part of this club")

    club = db.query(Club).filter(Club.id == club_id).first()
    if club.created_by != current_user.get_id():
        raise UnauthorizedException
    
    registration = db.query(Registration).filter(Registration.id == registration_id).first()
    if not registration:
        raise NotFoundException("Registration not found")
    
    form_response = db.query(FormResponse).filter(FormResponse.id == registration.form_response_id)
    team = db.query(Team).filter(Team.id == registration.team_id).first()
    team_members = db.query(TeamMember).filter(TeamMember.team_id == registration.team_id).all()

    registration.team = team
    registration.team.members = team_members
    registration.form_response = form_response

    return registration

def confirm_registration(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, registration_id: UUID) -> RegistrationSchema:
    registration = get_registration(current_user, db, club_id, event_id, registration_id)

    if registration.status == RegistrationStatusEnum.confirmed:
        raise ConflictException("Registration is already confirmed")

    registration.status = RegistrationStatusEnum.confirmed
    db.commit()
    db.refresh(registration)
    return registration

def cancel_registration(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, registration_id: UUID) -> RegistrationSchema:
    registration = get_registration(current_user, db, club_id, event_id, registration_id)

    if registration.status == RegistrationStatusEnum.cancelled:
        raise ConflictException("Registration is already cancelled")

    registration.status = RegistrationStatusEnum.cancelled
    db.commit()
    db.refresh(registration)
    return registration

def update_payment_status(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, registration_id: UUID, payment_status: str) -> RegistrationSchema:
    registration = get_registration(current_user, db, club_id, event_id, registration_id)

    if payment_status == "paid":
        registration.payment_status = PaymentStatusEnum.paid
        ts = int(datetime.now(timezone.utc).timestamp())
        registration.ticket_code = f"TICKET-{registration.id}-{ts}"
    elif payment_status == "unpaid":
        registration.payment_status = PaymentStatusEnum.unpaid
    elif payment_status == "refunded":
        registration.payment_status = PaymentStatusEnum.refunded
    else:
        raise BadRequestException(f"Invalid payment status")

    
    db.commit()
    db.refresh(registration)
    return registration

def get_registration_stats(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID):
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club_id).first()
    if not event:
        raise NotFoundException("Event not found or not part of this club")

    club = db.query(Club).filter(Club.id == club_id).first()
    if not club or club.created_by != current_user.get_id():
        raise UnauthorizedException

    total = db.query(Registration).filter(Registration.event_id == event_id).count()
    confirmed = db.query(Registration).filter(Registration.event_id == event_id, Registration.status == RegistrationStatusEnum.confirmed).count()
    cancelled = db.query(Registration).filter(Registration.event_id == event_id, Registration.status == RegistrationStatusEnum.cancelled).count()
    paid = db.query(Registration).filter(Registration.event_id == event_id, Registration.payment_status == PaymentStatusEnum.paid).count()
    unpaid = db.query(Registration).filter(Registration.event_id == event_id, Registration.payment_status == PaymentStatusEnum.unpaid).count()
    refunded = db.query(Registration).filter(Registration.event_id == event_id, Registration.payment_status == PaymentStatusEnum.refunded).count()

    return {
        "total_registrations": total,
        "confirmed": confirmed,
        "cancelled": cancelled,
        "paid": paid,
        "unpaid": unpaid,
        "refunded": refunded
    }