import traceback
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.deps import get_db
from app.schemas.club_schemas import ClubCreate, ClubSchema
from app.services.club_service import (
    create_club,
    get_club,
    get_club_by_slug,
    get_all_club,
    list_active_clubs,
    list_pending_clubs,
    approve_club,
    reject_club,
    update_club,
    delete_club,
)
from app.services.user_service import get_current_user
from app.schemas.user_schemas import TokenData
from app.exceptions.handler import (
    NotFoundException,
    ConflictException,
    EntityTooLargeException,
    BadRequestException,
    UnauthorizedException
)


club_router = APIRouter()


@club_router.post("/club/create", response_model=ClubSchema, status_code=201)
async def create_club_router(club: ClubCreate, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return create_club(current_user=current_user, payload=club, db=db)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise e


@club_router.get("/clubs", response_model=List[ClubSchema], status_code=200)
async def list_clubs_router(db: Session = Depends(get_db), skip: int = 0, limit: int = None):
    try:
        return list_active_clubs(db=db, skip=skip, limit=limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()

@club_router.get("/clubs/all", response_model=List[ClubSchema])
async def get_all_club_router(current_user: TokenData = Depends(get_current_user),skip: int = 0, limit: int = None, db: Session = Depends(get_db)):
    try:
        return get_all_club(current_user=current_user, db=db, skip=skip, limit=limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e

@club_router.get("/clubs/pending", response_model=List[ClubSchema])
async def list_pending_club_router(current_user: TokenData = Depends(get_current_user),skip: int = 0, limit: int = None, db: Session = Depends(get_db)):
    try:
        return list_pending_clubs(current_user=current_user, db=db, skip=skip, limit=limit)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        raise e


@club_router.get("/clubs/{slug}", response_model=ClubSchema)
async def get_club_router(slug: str, db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return get_club(db=db, club_id=club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise e

@club_router.patch("/clubs/{slug}", response_model=ClubSchema, status_code=201)
async def update_club_router(slug: str, club: ClubCreate, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return update_club(current_user=current_user, club_id=club_id, updated_attributes=club, db=db)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise e


@club_router.delete("/clubs/{slug}", status_code=204)
async def delete_club_router(slug: str, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        club_id = get_club_by_slug(slug=slug, db=db)
        return delete_club(current_user=current_user, db=db, club_id=club_id)
    except (NotFoundException, ConflictException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise e

@club_router.patch("/clubs/{slug}/approve", status_code=201)
async def approve_club_by_admin_router(slug: str, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    club_id = get_club_by_slug(slug=slug, db=db)
    club = approve_club(current_user=current_user,db=db, club_id=club_id)
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    return {"detail": f"Club {club.name} approved successfully"}

@club_router.patch("/clubs/{slug}/reject", status_code=201)
async def reject_club_by_admin_router(slug: str, current_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    club_id = get_club_by_slug(slug=slug, db=db)
    club = reject_club(current_user=current_user,db=db, club_id=club_id)
    if not club:
        raise NotFoundException(f"Club with id {club_id} not found")
    return {"detail": f"Club {club.name} rejected successfully"}

