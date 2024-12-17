from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import get_settings
from src.core.exceptions import setup_exception_handlers
from src.core.rate_limit import RateLimitMiddleware
from src.api import users, resumes, jobs
from fastapi.openapi.utils import get_openapi

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    Job Flow API is a powerful job-matching platform that helps users manage their job search efficiently.
    
    ## Features
    
    * **User Management**: Register, authenticate, and manage user profiles
    * **Resume Management**: Upload, parse, and enhance resumes using AI
    * **Job Matching**: Search and match jobs based on user profiles and preferences
    * **Insights**: Get personalized career insights and recommendations
    * **Notifications**: Receive real-time updates about job matches
    
    ## Authentication
    
    All API endpoints (except registration and login) require authentication using Firebase JWT tokens.
    Include the token in the Authorization header as: `Bearer <token>`.
    """,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.add_middleware(RateLimitMiddleware)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(
    users.router,
    prefix=f"{settings.API_V1_STR}/users",
    tags=["Users"],
    responses={
        401: {"description": "Authentication failed"},
        403: {"description": "Insufficient permissions"},
    }
)

app.include_router(
    resumes.router,
    prefix=f"{settings.API_V1_STR}/resumes",
    tags=["Resumes"],
    responses={
        401: {"description": "Authentication failed"},
        403: {"description": "Insufficient permissions"},
    }
)

app.include_router(
    jobs.router,
    prefix=f"{settings.API_V1_STR}/jobs",
    tags=["Jobs"],
    responses={
        401: {"description": "Authentication failed"},
        403: {"description": "Insufficient permissions"},
    }
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter the Firebase JWT token",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/",
    summary="Welcome endpoint",
    description="Returns a welcome message for the Job Flow API",
    response_description="Welcome message",
    tags=["Health"])
async def root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A dictionary containing a welcome message
    """
    return {"message": "Welcome to Job Flow API"}

@app.get("/health",
    summary="Health check endpoint",
    description="Checks if the API is running and healthy",
    response_description="Health status",
    tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: A dictionary containing the health status
    """
    return {"status": "healthy"}
