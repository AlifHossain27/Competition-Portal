from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user_router, club_router, event_router, form_router, form_response_router
from app.db.database import Base, engine

app = FastAPI(
    title = "Competition Portal",
    description = "An Competition Portal API",
    openapi_tags = False,
    version = "0.0.1",
    contact = {
        "name": "API Support",
        "url": "https://github.com/AlifHossain27",
        "email": "alifh044@gmail.com"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
Base.metadata.create_all(bind=engine)

app.include_router(user_router.user_router, prefix="/api", tags=["Users"])
app.include_router(club_router.club_router, prefix="/api", tags=["Clubs"])
app.include_router(event_router.event_router, prefix="/api", tags=["Events"])
app.include_router(form_router.form_router, prefix="/api", tags=["Forms"])
app.include_router(form_response_router.form_response_router, prefix="/api", tags=["FormResponses"])