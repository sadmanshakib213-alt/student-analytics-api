from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    id: Optional[int] = None
    name: str
    code: str
    credits: int
    description: Optional[str] = None

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    description: Optional[str] = None

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    description: Optional[str] = None