from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone
from app.models.club_model import Club
from app.models.event_model import Event
from app.models.team_model import Team, TeamMember
from app.schemas.team_schemas import TeamSchema, TeamMemberSchema, TeamBase, TeamMemberBase
from app.schemas.user_schemas import TokenData
from app.exceptions.handler import (
    UnauthorizedException,
    NotFoundException,
    ConflictException,
    BadRequestException
)


def verify_club_event_access(db: Session, current_user: TokenData, club_id: UUID, event_id: UUID):
    event = db.query(Event).filter(Event.id == event_id, Event.club_id == club_id).first()
    if not event:
        raise NotFoundException("Event not found or not part of this club")

    club = db.query(Club).filter(Club.id == club_id).first()
    if not club or club.created_by != current_user.get_id():
        raise UnauthorizedException

    return event


def get_all_teams(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID) -> list[TeamSchema]:
    verify_club_event_access(db, current_user, club_id, event_id)
    teams = db.query(Team).filter(Team.event_id == event_id).all()
    for team in teams:
        team.members = db.query(TeamMember).filter(TeamMember.team_id == team.id).all()
    return teams


def get_team(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, team_id: UUID) -> TeamSchema:
    verify_club_event_access(db, current_user, club_id, event_id)
    team = db.query(Team).filter(Team.id == team_id, Team.event_id == event_id).first()
    if not team:
        raise NotFoundException("Team not found in this event")

    team.members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
    return team


def update_team_info(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, team_id: UUID, update_data: TeamBase):
    verify_club_event_access(db, current_user, club_id, event_id)
    team = db.query(Team).filter(Team.id == team_id, Team.event_id == event_id).first()
    if not team:
        raise NotFoundException("Team not found")

    team.team_name = update_data.team_name
    team.leader_name = update_data.leader_name
    team.leader_email = update_data.leader_email
    team.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(team)
    return team


def get_team_members(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, team_id: UUID) -> list[TeamMemberSchema]:
    verify_club_event_access(db, current_user, club_id, event_id)
    team = db.query(Team).filter(Team.id == team_id, Team.event_id == event_id).first()
    if not team:
        raise NotFoundException("Team not found")

    members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
    return members


def update_team_member(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, member_id: UUID, update_data: TeamMemberBase):
    verify_club_event_access(db, current_user, club_id, event_id)
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise NotFoundException("Team member not found")

    member.member_name = update_data.member_name
    member.member_email = update_data.member_email
    member.member_student_id = update_data.member_student_id
    member.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(member)
    return member


def delete_team_member(current_user: TokenData, db: Session, club_id: UUID, event_id: UUID, member_id: UUID):
    verify_club_event_access(db, current_user, club_id, event_id)
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise NotFoundException("Team member not found")

    db.delete(member)
    db.commit()
    return {"message": "Team member removed successfully"}
