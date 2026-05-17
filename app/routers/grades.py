from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.grade import Grade, GradeCreate, GradeUpdate, GPAResponse

router = APIRouter()

# In-memory database
grades_db = {}
counter = 1

@router.get("/", response_model=List[Grade])
def get_all_grades():
    return list(grades_db.values())

@router.get("/{grade_id}", response_model=Grade)
def get_grade(grade_id: int):
    if grade_id not in grades_db:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grades_db[grade_id]

@router.post("/", response_model=Grade)
def create_grade(grade: GradeCreate):
    global counter
    new_grade = Grade(id=counter, **grade.dict())
    grades_db[counter] = new_grade
    counter += 1
    return new_grade

@router.put("/{grade_id}", response_model=Grade)
def update_grade(grade_id: int, grade: GradeUpdate):
    if grade_id not in grades_db:
        raise HTTPException(status_code=404, detail="Grade not found")
    existing = grades_db[grade_id]
    updated_data = grade.dict(exclude_unset=True)
    updated_grade = existing.copy(update=updated_data)
    grades_db[grade_id] = updated_grade
    return updated_grade

@router.delete("/{grade_id}")
def delete_grade(grade_id: int):
    if grade_id not in grades_db:
        raise HTTPException(status_code=404, detail="Grade not found")
    del grades_db[grade_id]
    return {"message": f"Grade {grade_id} deleted successfully"}

@router.get("/student/{student_id}/gpa", response_model=GPAResponse)
def calculate_gpa(student_id: int, semester: Optional[str] = None):
    student_grades = [
        g for g in grades_db.values()
        if g.student_id == student_id
        and (semester is None or g.semester == semester)
    ]
    if not student_grades:
        raise HTTPException(
            status_code=404,
            detail="No grades found for this student"
        )
    gpa = sum(g.grade for g in student_grades) / len(student_grades)
    return GPAResponse(
        student_id=student_id,
        gpa=round(gpa, 2),
        total_courses=len(student_grades),
        semester=semester
    )