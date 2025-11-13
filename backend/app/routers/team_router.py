from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.deps import get_db
from app.schemas.user_schemas import TokenData
from app.schemas.team_schemas import TeamSchema, TeamMemberSchema, TeamBase, TeamMemberBase
from app.services.team_service import (
    get_all_teams,
    get_team,
    update_team_info,
    get_team_members,
    update_team_member,
    delete_team_member,
)
from app.services.user_service import get_current_user
from app.services.club_service import get_club_by_slug
from app.exceptions.handler import (
    NotFoundException,
    ConflictException,
    EntityTooLargeException,
    BadRequestException,
    UnauthorizedException
)


team_router = APIRouter()


@team_router.get("/club/{slug}/event/{event_id}/team", response_model=list[TeamSchema], status_code=200)
async def list_teams(slug: str, event_id: UUID, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_all_teams(current_user, db, club_id, event_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e


@team_router.get("/club/{slug}/event/{event_id}/team/{team_id}", response_model=TeamSchema, status_code=200)
async def get_team(slug: str, event_id: UUID, team_id: UUID, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_team(current_user, db, club_id, event_id, team_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e


@team_router.patch("/club/{slug}/event/{event_id}/team/{team_id}", response_model=TeamSchema, status_code=201)
async def edit_team(slug: str, event_id: UUID, team_id: UUID, team_data: TeamBase, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return update_team_info(current_user, db, club_id, event_id, team_id, team_data)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e


@team_router.get("/club/{slug}/event/{event_id}/team/{team_id}/members", response_model=list[TeamMemberSchema] , status_code=200)
async def list_team_members(slug: str, event_id: UUID, team_id: UUID, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_team_members(current_user, db, club_id, event_id, team_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e


@team_router.patch("/club/{slug}/event/{event_id}/team/{team_id}/members/{member_id}", response_model=TeamMemberSchema, status_code=201)
async def edit_team_member(slug: str, event_id: UUID, team_id: UUID, member_id: UUID, member_data: TeamMemberBase, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return update_team_member(current_user, db, club_id, event_id, team_id, member_id, member_data)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e


@team_router.delete("/club/{slug}/event/{event_id}/team/{team_id}/members/{member_id}", status_code=204)
async def remove_team_member(slug: str, event_id: UUID, team_id: UUID, member_id: UUID, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return delete_team_member(current_user, db, club_id, event_id, team_id, member_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e