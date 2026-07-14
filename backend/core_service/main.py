import sys, os

# Add all subdirectories to path once — before any other imports
_base = os.path.dirname(__file__)
for _folder in ["", "models", "schemas", "services", "routers", "controllers", "repositories", "middleware"]:
    _p = os.path.join(_base, _folder)
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base

# Import models ONCE so SQLAlchemy registers them
import user_model        # noqa: F401
import arrangement_model # noqa: F401

from routers import auth_router, arrangements_router


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
