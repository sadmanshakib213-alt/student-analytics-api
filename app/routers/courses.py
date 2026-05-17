from fastapi import APIRouter, HTTPException
from typing import List
from app.models.course import Course, CourseCreate, CourseUpdate

router = APIRouter()

# In-memory database
courses_db = {}
counter = 1

@router.get("/", response_model=List[Course])
def get_all_courses():
    return list(courses_db.values())

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses_db[course_id]

@router.post("/", response_model=Course)
def create_course(course: CourseCreate):
    global counter
    new_course = Course(id=counter, **course.dict())
    courses_db[counter] = new_course
    counter += 1
    return new_course

@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, course: CourseUpdate):
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    existing = courses_db[course_id]
    updated_data = course.dict(exclude_unset=True)
    updated_course = existing.copy(update=updated_data)
    courses_db[course_id] = updated_course
    return updated_course

@router.delete("/{course_id}")
def delete_course(course_id: int):
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses_db[course_id]
    return {"message": f"Course {course_id} deleted successfully"}