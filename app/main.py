from fastapi import FastAPI
from app.routers import students, courses, grades
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Student Analytics API",
    description="A production-grade API for managing student performance analytics",
    version="1.0.0"
)

# Include routers
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(grades.router, prefix="/api/v1/grades", tags=["Grades"])

# Prometheus monitoring
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Student Analytics API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}