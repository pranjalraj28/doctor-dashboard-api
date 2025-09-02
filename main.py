import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.Database import db_manager
from app.api.AuthApi import router as auth_router
from app.api.DoctorApi import router as doctor_router
from app.core.config import settings
from app.core.exceptions import (
    DoctorDashboardError,
    AuthenticationError,
    AuthorizationError,
    DoctorNotFoundError,
    DuplicateError,
    ValidationError,
    DatabaseError
)
from app.api import PatientApi, VisitApi
from fastapi.openapi.utils import get_openapi
from app.models import Doctor, Patient, Visit, DoctorPatientAssignment

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the default logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    db_manager.init_db()
    yield
    # Shutdown
    await db_manager.close()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_router, prefix=settings.api_v1_str)
    app.include_router(doctor_router, prefix=settings.api_v1_str)
    app.include_router(PatientApi.router, prefix=settings.api_v1_str)
    app.include_router(VisitApi.router, prefix=settings.api_v1_str)
    
    # Exception handlers
    @app.exception_handler(DuplicateError)
    async def duplicate_error_handler(request: Request, exc: DuplicateError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc), "type": "duplicate_error"}
        )
    
    @app.exception_handler(DoctorNotFoundError)
    async def doctor_not_found_handler(request: Request, exc: DoctorNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc), "type": "not_found_error"}
        )
    
    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc), "type": "authentication_error"},
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @app.exception_handler(AuthorizationError)
    async def authorization_error_handler(request: Request, exc: AuthorizationError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc), "type": "authorization_error"}
        )
    
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc), "type": "validation_error"}
        )
    
    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred", "type": "database_error"}
        )
    
    @app.exception_handler(DoctorDashboardError)
    async def general_error_handler(request: Request, exc: DoctorDashboardError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc), "type": "application_error"}
        )
    
    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": settings.app_version}
    
    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint."""
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs_url": "/docs" if settings.debug else "Documentation disabled in production"
        }
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=settings.app_name,
            version=settings.app_version,
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "OAuth2Password": {
                "type": "oauth2",
                "flows": {
                 "password": {
                    "tokenUrl": f"{settings.api_v1_str}/auth/login",
                    "scopes": {}
                    }
                }
            }
        }
    # Secure all endpoints by default, or customize per route if needed
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method["security"] = [{"OAuth2Password": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    
    return app


# Create the application instance
app = create_application()