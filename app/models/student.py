from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class Student(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: int
    role: RoleEnum = RoleEnum.student

class StudentCreate(BaseModel):
    name: str
    email: str
    age: int
    role: RoleEnum = RoleEnum.student

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    role: Optional[RoleEnum] = None