from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from database import  get_db, engine
from sqlalchemy.orm import Session
import models

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

@app.get("/")
def home():
    return "Hello world"

class Student(BaseModel):
    student_id : str = Field(...)
    name : str = Field(max_length=50)
    course : str = Field(max_length=100)
    marks : int = Field(le = 100, ge = 0)

@app.post("/student/", status_code=201, tags=["Student"])
def create_student(student:Student, db:Session = Depends(get_db)):  
    new_student = models.Student(
        id = student.student_id,
        name = student.name,
        course = student.course,
        marks = student.marks
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {"message":"Student created successfully","student":student}

@app.get("/student/",tags=["Student"])
def get_students(db:Session = Depends(get_db)):
    
    students = db.query(models.Student).all()

    return students


@app.get("/student/{student_id}", tags=["Student"])
def get_student(student_id : str, db:Session = Depends(get_db)):

    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code= 404,
            detail=f"Student with {student_id} not found"
        )
    
    return student