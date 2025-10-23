from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.club_model import Club, ClubStatusEnum
from app.models.user_model import User, UserRoleEnum
from app.schemas.club_schemas import ClubCreate, ClubSchema
from app.schemas.user_schemas import TokenData
from app.services.user_service import (
    get_user_by_uuid,
    CurrentUser
)
from app.exceptions.handler import (
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
    ConflictException
)


def create_club(current_user:TokenData, db: Session, payload: ClubCreate) -> ClubSchema:
    user_club = db.query(Club).filter(Club.created_by == current_user.get_id()).first()
    if user_club is not None:
        raise ConflictException("User already has a club")
    
    club = Club(
        name=payload.name,
        slug=payload.slug,
        description=payload.description,
        logo_url=str(payload.logo_url) if payload.logo_url else None,
        banner_url=str(payload.banner_url) if payload.banner_url else None,
        website=str(payload.website) if payload.website else None,
        created_by=current_user.get_id(),
    )
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


def get_club(db: Session, club_id: UUID) -> ClubSchema:
    club = db.query(Club).filter(Club.id == club_id).first()
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    return club


def list_active_clubs(db: Session, skip: int = 0, limit: int = None) -> List[ClubSchema]:
    return db.query(Club).filter(Club.status == ClubStatusEnum.active).offset(skip).limit(limit).all()


def list_pending_clubs(current_user:TokenData, db: Session, skip: int = 0, limit: int = None) -> List[ClubSchema]:
    user = get_user_by_uuid(uuid=current_user.get_id(), db=db)
    if user.role == UserRoleEnum.admin:
        return db.query(Club).filter(Club.status == ClubStatusEnum.pending).offset(skip).limit(limit).all()
    else:
        raise UnauthorizedException("Admin user required")
    
def get_all_club(current_user:TokenData, db: Session, skip: int = 0, limit: int = None) -> List[ClubSchema]:
    user = get_user_by_uuid(uuid=current_user.get_id(), db=db)
    if user.role == UserRoleEnum.admin:
        return db.query(Club).offset(skip).limit(limit).all()
    else:
        raise UnauthorizedException("Admin user required")

# Approve a club
def approve_club(current_user:TokenData, db: Session, club_id: UUID):
    uuid = current_user.get_id()
    user = get_user_by_uuid(uuid=uuid, db=db)
    if user.role == UserRoleEnum.admin:
        club = db.query(Club).filter(Club.id == club_id).first()
        if not club:
            return None
        club.status = ClubStatusEnum.active
        club.approved_by = user.id
        user.role = UserRoleEnum.club
        db.commit()
        db.refresh(club)
        return club
    else:
        raise UnauthorizedException("Admin user required")
    

# Reject a club
def reject_club(current_user:TokenData, db: Session, club_id: UUID):
    uuid = current_user.get_id()
    user = get_user_by_uuid(uuid=uuid, db=db)
    if user.role == UserRoleEnum.admin:
        club = db.query(Club).filter(Club.id == club_id).first()
        if not club:
            return None
        club.status = ClubStatusEnum.rejected
        club.approved_by = user.id
        db.commit()
        db.refresh(club)
        return club
    else:
        raise UnauthorizedException("Admin user required")


def update_club(current_user:TokenData, club_id: UUID, updated_attributes: ClubCreate, db:Session) -> ClubSchema:
    user = get_user_by_uuid(uuid=current_user.get_id(), db=db)
    club = db.query(Club).filter(Club.id == club_id).first()
    if club is None:
        raise NotFoundException(f"Club with id {club_id} not found")
    if club.created_by != user.id:
        raise UnauthorizedException("You are not the creator of this club")
    club.name = updated_attributes.name
    club.slug = updated_attributes.slug
    club.description = updated_attributes.description
    club.logo_url = updated_attributes.logo_url
    club.banner_url = updated_attributes.banner_url
    club.website = updated_attributes.website

    db.commit()
    db.refresh(club)

    return club


def delete_club(current_user:TokenData, db: Session, club_id: UUID) -> None:
    user = get_user_by_uuid(uuid=current_user.get_id(), db=db)
    club = db.query(Club).filter(Club.id == club_id).first()
    if club is None:
        raise NotFoundException(f"Club with id {club_id} not found")
    if club.created_by != user.id:
        raise UnauthorizedException("You are not the creator of this club")
    db.delete(club)
    db.commit()
