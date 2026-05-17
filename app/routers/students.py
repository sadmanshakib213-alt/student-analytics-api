from fastapi import APIRouter, HTTPException
from typing import List
from app.models.student import Student, StudentCreate, StudentUpdate

router = APIRouter()

# In-memory database
students_db = {}
counter = 1

@router.get("/", response_model=List[Student])
def get_all_students():
    return list(students_db.values())

@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

@router.post("/", response_model=Student)
def create_student(student: StudentCreate):
    global counter
    new_student = Student(id=counter, **student.dict())
    students_db[counter] = new_student
    counter += 1
    return new_student

@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentUpdate):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    existing = students_db[student_id]
    updated_data = student.dict(exclude_unset=True)
    updated_student = existing.copy(update=updated_data)
    students_db[student_id] = updated_student
    return updated_student

@router.delete("/{student_id}")
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return {"message": f"Student {student_id} deleted successfully"}