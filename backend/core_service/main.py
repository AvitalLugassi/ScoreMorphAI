from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .routers import auth_router, arrangements_router

# Import models so SQLAlchemy registers them before create_all
from .models import User, Arrangement  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(
        title="ScoreMorphAI — Core Service",
        version="1.0.0",
        docs_url="/docs" if settings.APP_ENV != "production" else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def create_tables():
        Base.metadata.create_all(bind=engine)

    app.include_router(auth_router)
    app.include_router(arrangements_router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "core_service"}

    return app


app = create_app()
