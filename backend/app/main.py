from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, health, holdings, products, transactions, users


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="API for structured investment products, holdings, and transactions.",
        openapi_tags=[
            {"name": "health", "description": "Service health checks"},
            {"name": "auth", "description": "Registration and JWT login"},
            {"name": "users", "description": "Authenticated user profile"},
            {"name": "products", "description": "Structured product catalog CRUD"},
            {"name": "holdings", "description": "Portfolio holding CRUD"},
            {"name": "transactions", "description": "Transaction CRUD"},
        ],
    )

    Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(products.router, prefix="/products", tags=["products"])
    app.include_router(holdings.router, prefix="/holdings", tags=["holdings"])
    app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
    return app


app = create_app()

