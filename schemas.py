from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):

    title: str = Field(min_length=1, max_length=200)

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )


class TaskUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    completed: Optional[bool] = None


class TaskResponse(BaseModel):

    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    
    