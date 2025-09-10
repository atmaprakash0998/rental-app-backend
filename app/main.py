from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .features.auth.routes import router as auth_router
from .core.middleware import AuthMiddleware
from .features.vehicles.routes import router as vehicles_router
from .features.documents.routes import router as documents_router
from .features.settings.routes import router as settings_router



def create_app() -> FastAPI:
    app = FastAPI(title="Rental App Backend", version="0.2.0")

    allowed_origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add authentication middleware
    app.add_middleware(AuthMiddleware)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    @app.get("/api/v1/greeting")
    async def greeting(name: str = "there") -> dict:
        return {"message": f"Hello, {name}! From FastAPI backend."}


    # Include routes
    app.include_router(auth_router)
    app.include_router(vehicles_router)
    app.include_router(documents_router)
    app.include_router(settings_router)
    
    return app


app = create_app()


