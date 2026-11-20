import sqlite3
from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel, Field , StringConstraints
from contextlib import closing
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = Path(__file__).with_name("students.db")

app = FastAPI()
"""
students = [
            {"id" : 1, "name" : "Bob Smith", "course" : "Python", "age" : 25 },
            {"id" : 2, "name" : "Captain Jack Sparrow", "course" : "React", "age" : 25},
            {"id" : 3, "name" : "John Doe", "course" : "Angular", "age" : 30},
            {"id" : 4, "name" : "Jane Smith", "course" : "Vue.js", "age" : 28}
           ]
"""


origins = [
    "http://localhost:3000",  # React/Next.js default
    "http://localhost:5173",  # Vite/Vue default
    "http://127.0.0.1:5500",  # VS Code Live Server default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use ["*"] to allow all origins during testing
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods, including OPTIONS, GET, POST, etc.
    allow_headers=["*"],    # Allows all headers
)


@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}


@app.get("/students")
def get_students():
    with closing(sqlite3.connect(DB_PATH)) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("SELECT id, name, course, age FROM students ORDER BY id").fetchall()
    return [dict(row) for row in rows]
    #return students


#Return a student based on their ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    with closing(sqlite3.connect(DB_PATH)) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("SELECT id, name, course, age FROM students WHERE id = ? ORDER BY id", (student_id,)).fetchall()
    return [dict(row) for row in rows]


#Create a student data model from this class
class StudentCreate(BaseModel):
    name:Annotated[str , StringConstraints( strip_whitespace=True,min_length= 1)]
    course:Annotated[str , StringConstraints( strip_whitespace=True,min_length= 1), Field(default="JavaScript")]
    age: int = Field(default = 18)
#Add student to the DB
@app.post("/students", status_code=201)
async def create_student(student : StudentCreate):
    with closing(sqlite3.connect(DB_PATH)) as db:
        result = db.execute(
            "INSERT INTO students (name, course, age) VALUES (?,?,?)",
            (student.name, student.course, student.age,),
        )
        db.commit()
    return {"id": result.lastrowid, "name": student.name, "course": student.course, "age": student.age}
    """
    new_student = {
        "id" : len(students) + 1,
        "name" : student.name,
        "course" : student.course,
        "age" : student.age
    }
    students.append(new_student)
    return new_student
    """


@app.delete("/students/{id}")
def delete_student(id : int):
    try:
        with closing(sqlite3.connect(DB_PATH)) as db:
            cursor = db.execute("DELETE FROM students WHERE id = ?", (id,))
            db.commit()
        return "Rows Deleted: " + str(cursor.rowcount), "See the remaining students here", get_students()
    except sqlite3.Error as e:
        return(f"Database error: {e}")
    except Exception as e:       
        return(f"An unexpected error occurred: {e}")
    """
    for student in students:
        if student["id"] == id:
            students.remove(student)
            return "The following student has been deleted: " + str(student), "See the remaining students here", students
    
    return {"error" : "Student not found"}
    """