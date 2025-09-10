from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

# In-memory storage for notes for this stage of the project.
# This should be replaced by a database-backed repository in future iterations.
_NOTES_DB: List["Note"] = []


class NoteBase(BaseModel):
    """Base fields for a note."""
    title: str = Field(..., description="Title of the note", min_length=1, max_length=255)
    content: str = Field(..., description="Content/body of the note")


class NoteCreate(NoteBase):
    """Payload for creating a new note."""
    # Additional fields like tags, user_id can be added later
    pass


class Note(NoteBase):
    """A note entity returned by the API."""
    id: str = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Creation timestamp in UTC")
    updated_at: datetime = Field(..., description="Last update timestamp in UTC")


router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"],
)


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Creates a new note with a unique identifier and timestamps, and returns the created note.",
    responses={
        201: {
            "description": "Note created successfully",
        },
        400: {
            "description": "Invalid input provided",
        },
    },
)
def create_note(payload: NoteCreate) -> Note:
    """
    Create a new note.

    Parameters:
    - payload: NoteCreate - The note details to create, including title and content.

    Returns:
    - Note: The created note object with id, timestamps, title, and content.

    Notes:
    - For now, data is stored in-memory. In future iterations, this should use a persistent database layer.
    """
    now = datetime.utcnow()
    note = Note(
        id=str(uuid4()),
        title=payload.title,
        content=payload.content,
        created_at=now,
        updated_at=now,
    )
    _NOTES_DB.append(note)
    return note
