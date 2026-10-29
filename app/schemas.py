from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False
    priority: int = Field(default=1, ge=1, le=5)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    done: Optional[bool] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)

class TaskOut(BaseModel):
    id: int
    title: str
    done: bool
    priority: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class StudentCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=200)
    second_name: str = Field(min_length=1, max_length=200)
    group: int = Field(default=1, ge=1, le=2)
    course: int = Field(default=1, ge=1, le=4)

class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    second_name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    group: Optional[int] = Field(default=1, ge=1, le=2)
    course: Optional[int] = Field(default=1, ge=1, le=4)
