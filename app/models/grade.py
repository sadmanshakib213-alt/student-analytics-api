from pydantic import BaseModel
from typing import Optional

class Grade(BaseModel):
    id: Optional[int] = None
    student_id: int
    course_id: int
    grade: float
    semester: str

class GradeCreate(BaseModel):
    student_id: int
    course_id: int
    grade: float
    semester: str

class GradeUpdate(BaseModel):
    grade: Optional[float] = None
    semester: Optional[str] = None

class GPAResponse(BaseModel):
    student_id: int
    gpa: float
    total_courses: int
    semester: Optional[str] = None