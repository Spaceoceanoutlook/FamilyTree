from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: str | None = Field(None, max_length=255)
    message: str = Field(..., min_length=1)


class FeedbackOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
