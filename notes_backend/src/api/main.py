from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.notes import router as notes_router

app = FastAPI(
    title="Personal Notes Backend",
    description="RESTful API for managing personal notes and users.",
    version="0.1.0",
    openapi_tags=[
        {"name": "Health", "description": "Health and diagnostics endpoints"},
        {"name": "Notes", "description": "CRUD operations for notes"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Returns a simple health status to indicate the service is up.",
)
def health_check():
    """Health check endpoint for service liveness."""
    return {"message": "Healthy"}


# Register routers
app.include_router(notes_router)
