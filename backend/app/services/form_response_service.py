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
from app.schemas.registration_schemas import RegistrationFullSchema
from app.schemas.user_schemas import TokenData
from app.exceptions.handler import (
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
    ConflictException,
    ForbiddenException
)

def create_form_response(db: Session, response_data: FormResponseCreate, form_id: UUID, event_id: UUID, club_id: UUID) -> RegistrationFullSchema:
    form = db.query(Form).filter(Form.id == form_id).first()

    if not form:
        raise NotFoundException(f"Form with ID {form_id} not found")
    
    if form.status != FormStatusEnum.published:
        raise BadRequestException("Form must be published to accept responses.")
    
    if response_data.members:
        for member in response_data.members:
            existing_member = (
                db.query(TeamMember)
                .join(Team, Team.id == TeamMember.team_id)
                .filter(
                    Team.event_id == event_id,
                    (TeamMember.member_email == member.member_email)
                    | (TeamMember.member_student_id == member.member_student_id)
                )
                .first()
            )
            if existing_member:
                raise ConflictException(
                    f"Member {member.member_name} ({member.member_email}) already registered for this event."
                )
            
    team = Team(
        event_id=event_id,
        team_name=response_data.team_name,
        leader_name=response_data.leader_name,
        leader_email=response_data.leader_email
    )
    db.add(team)
    db.commit()
    db.refresh(team)

    for member in response_data.members:
        new_member = TeamMember(
            team_id=team.id,
            member_name=member.member_name,
            member_email=member.member_email,
            member_student_id=member.member_student_id
        )
        db.add(new_member)
    db.commit()
            
    form_response = FormResponse(
        form_id=form_id,
        response_content=response_data.response_content,
    )
    db.add(form_response)
    db.commit()
    db.refresh(form_response)

    registration = Registration(
        event_id=event_id,
        form_response_id=form_response.id,
        team_id=team.id,
        status=RegistrationStatusEnum.pending,
        payment_status=PaymentStatusEnum.unpaid,
        ticket_code=None
    )
    db.add(registration)
    db.commit()
    db.refresh(registration)

    registration.team = team
    registration.team.members = db.query(TeamMember).filter(TeamMember.team_id == team.id).all()
    registration.form_response = form_response

    return registration

def list_form_responses(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, form_id: UUID) -> list[FormResponseSchema]:
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club_id).first()
    if not event:
        raise NotFoundException("Event not found or not part of this club")
    
    club = db.query(Club).filter(Club.id == club_id).first()
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    responses = db.query(FormResponse).filter(FormResponse.form_id == form_id).all()
    return responses

def get_form_response(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, form_id: UUID, response_id: UUID) -> FormResponseSchema:
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club_id).first()
    if not event:
        raise NotFoundException("Event not found or not part of this club")
    
    club = db.query(Club).filter(Club.id == club_id).first()
    if club.created_by != current_user.get_id():
        raise UnauthorizedException

    response = db.query(FormResponse).filter(
        FormResponse.id == response_id,
        FormResponse.form_id == form_id
    ).first()

    if not response:
        raise NotFoundException("Form response not found")

    return response