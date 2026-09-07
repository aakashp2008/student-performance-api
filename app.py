from typing import Optional

import sqlite3

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import uvicorn


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app = FastAPI(
    title="Student Performance API",
    description=(
        "A REST API for managing student academic performance, "
        "calculating GPA, and analyzing student results."
    ),
    version="1.0.0"
)

DATABASE_NAME = "students.db"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            marks REAL NOT NULL,
            attendance REAL NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


initialize_database()


# ============================================================
# PYDANTIC MODELS
# ============================================================

class StudentCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: str = Field(
        ...,
        min_length=5,
        max_length=150
    )

    department: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    year: int = Field(
        ...,
        ge=1,
        le=5
    )

    marks: float = Field(
        ...,
        ge=0,
        le=100
    )

    attendance: float = Field(
        ...,
        ge=0,
        le=100
    )


class StudentUpdate(BaseModel):

    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100
    )

    email: Optional[str] = Field(
        None,
        min_length=5,
        max_length=150
    )

    department: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50
    )

    year: Optional[int] = Field(
        None,
        ge=1,
        le=5
    )

    marks: Optional[float] = Field(
        None,
        ge=0,
        le=100
    )

    attendance: Optional[float] = Field(
        None,
        ge=0,
        le=100
    )


# ============================================================
# GPA CALCULATION
# ============================================================

def calculate_gpa(marks: float) -> float:

    if marks >= 90:
        return 10.0

    elif marks >= 80:
        return 9.0

    elif marks >= 70:
        return 8.0

    elif marks >= 60:
        return 7.0

    elif marks >= 50:
        return 6.0

    elif marks >= 40:
        return 5.0

    else:
        return 0.0


# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================

def get_performance_level(
    marks: float,
    attendance: float
):

    if marks >= 90 and attendance >= 90:

        return "Outstanding"

    elif marks >= 80 and attendance >= 80:

        return "Excellent"

    elif marks >= 70 and attendance >= 75:

        return "Good"

    elif marks >= 50:

        return "Average"

    else:

        return "Needs Improvement"


def get_recommendations(
    marks: float,
    attendance: float
):

    recommendations = []

    if marks < 50:

        recommendations.append(
            "Focus on improving academic performance."
        )

    elif marks < 70:

        recommendations.append(
            "Increase study consistency to improve marks."
        )

    elif marks < 80:

        recommendations.append(
            "Maintain your performance and target higher grades."
        )

    else:

        recommendations.append(
            "Excellent academic performance. Keep progressing."
        )

    if attendance < 75:

        recommendations.append(
            "Improve attendance to meet the recommended level."
        )

    elif attendance < 85:

        recommendations.append(
            "Try to maintain attendance above 85%."
        )

    else:

        recommendations.append(
            "Good attendance. Maintain consistency."
        )

    return recommendations


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def student_to_dict(student):

    marks = student["marks"]
    attendance = student["attendance"]

    gpa = calculate_gpa(marks)

    performance = get_performance_level(
        marks,
        attendance
    )

    recommendations = get_recommendations(
        marks,
        attendance
    )

    return {
        "id": student["id"],
        "name": student["name"],
        "email": student["email"],
        "department": student["department"],
        "year": student["year"],
        "marks": marks,
        "attendance": attendance,
        "gpa": gpa,
        "performance_level": performance,
        "recommendations": recommendations
    }


def find_student(student_id: int):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM students
        WHERE id = ?
        """,
        (student_id,)
    )

    student = cursor.fetchone()

    connection.close()

    return student


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Welcome to Student Performance API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "database": DATABASE_NAME
    }


# ============================================================
# CREATE STUDENT
# ============================================================

@app.post(
    "/students",
    status_code=201
)
def create_student(student: StudentCreate):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO students
            (name, email, department, year, marks, attendance)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student.name,
                student.email,
                student.department,
                student.year,
                student.marks,
                student.attendance
            )
        )

        connection.commit()

        student_id = cursor.lastrowid

    except sqlite3.IntegrityError:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="A student with this email already exists."
        )

    connection.close()

    created_student = find_student(student_id)

    return {
        "message": "Student created successfully",
        "student": student_to_dict(created_student)
    }


# ============================================================
# GET ALL STUDENTS
# ============================================================

@app.get("/students")
def get_students(
    department: Optional[str] = Query(
        None,
        description="Filter by department"
    ),

    year: Optional[int] = Query(
        None,
        ge=1,
        le=5,
        description="Filter by academic year"
    ),

    min_marks: Optional[float] = Query(
        None,
        ge=0,
        le=100,
        description="Minimum marks"
    )
):

    connection = get_connection()

    cursor = connection.cursor()

    query = "SELECT * FROM students WHERE 1=1"

    parameters = []

    if department:

        query += " AND department = ?"

        parameters.append(department)

    if year:

        query += " AND year = ?"

        parameters.append(year)

    if min_marks is not None:

        query += " AND marks >= ?"

        parameters.append(min_marks)

    query += " ORDER BY marks DESC"

    cursor.execute(
        query,
        parameters
    )

    students = cursor.fetchall()

    connection.close()

    return {
        "count": len(students),
        "students": [
            student_to_dict(student)
            for student in students
        ]
    }


# ============================================================
# GET STUDENT BY ID
# ============================================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    student = find_student(student_id)

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    return {
        "student": student_to_dict(student)
    }


# ============================================================
# UPDATE STUDENT
# ============================================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentUpdate
):

    existing_student = find_student(student_id)

    if not existing_student:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    update_data = student.model_dump(
        exclude_unset=True
    )

    if not update_data:

        raise HTTPException(
            status_code=400,
            detail="No update data provided."
        )

    connection = get_connection()

    cursor = connection.cursor()

    fields = []

    values = []

    for field, value in update_data.items():

        fields.append(
            f"{field} = ?"
        )

        values.append(value)

    values.append(student_id)

    query = f"""
        UPDATE students
        SET {", ".join(fields)}
        WHERE id = ?
    """

    try:

        cursor.execute(
            query,
            values
        )

        connection.commit()

    except sqlite3.IntegrityError:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="A student with this email already exists."
        )

    connection.close()

    updated_student = find_student(student_id)

    return {
        "message": "Student updated successfully",
        "student": student_to_dict(updated_student)
    }


# ============================================================
# DELETE STUDENT
# ============================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    existing_student = find_student(student_id)

    if not existing_student:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM students
        WHERE id = ?
        """,
        (student_id,)
    )

    connection.commit()

    connection.close()

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }


# ============================================================
# STUDENT PERFORMANCE ANALYSIS
# ============================================================

@app.get(
    "/students/{student_id}/performance"
)
def analyze_student_performance(
    student_id: int
):

    student = find_student(student_id)

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    marks = student["marks"]

    attendance = student["attendance"]

    gpa = calculate_gpa(marks)

    performance = get_performance_level(
        marks,
        attendance
    )

    recommendations = get_recommendations(
        marks,
        attendance
    )

    return {

        "student_id":
            student["id"],

        "student_name":
            student["name"],

        "academic_performance": {

            "marks":
                marks,

            "gpa":
                gpa,

            "performance_level":
                performance

        },

        "attendance": {

            "percentage":
                attendance,

            "status":
                "Good"
                if attendance >= 75
                else "Low"

        },

        "recommendations":
            recommendations

    }


# ============================================================
# TOP PERFORMERS
# ============================================================

@app.get("/students/top-performers")
def get_top_performers(
    limit: int = Query(
        5,
        ge=1,
        le=50
    )
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM students
        ORDER BY marks DESC
        LIMIT ?
        """,
        (limit,)
    )

    students = cursor.fetchall()

    connection.close()

    return {
        "count": len(students),
        "top_performers": [
            student_to_dict(student)
            for student in students
        ]
    }


# ============================================================
# DEPARTMENT STATISTICS
# ============================================================

@app.get("/statistics")
def get_statistics():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_students,
            AVG(marks) AS average_marks,
            AVG(attendance) AS average_attendance,
            MAX(marks) AS highest_marks,
            MIN(marks) AS lowest_marks
        FROM students
        """
    )

    statistics = cursor.fetchone()

    cursor.execute(
        """
        SELECT
            department,
            COUNT(*) AS student_count,
            AVG(marks) AS average_marks
        FROM students
        GROUP BY department
        ORDER BY average_marks DESC
        """
    )

    departments = cursor.fetchall()

    connection.close()

    return {

        "overall_statistics": {

            "total_students":
                statistics["total_students"],

            "average_marks":
                round(
                    statistics["average_marks"] or 0,
                    2
                ),

            "average_attendance":
                round(
                    statistics["average_attendance"] or 0,
                    2
                ),

            "highest_marks":
                statistics["highest_marks"] or 0,

            "lowest_marks":
                statistics["lowest_marks"] or 0

        },

        "department_statistics": [

            {
                "department":
                    department["department"],

                "student_count":
                    department["student_count"],

                "average_marks":
                    round(
                        department["average_marks"],
                        2
                    )

            }

            for department in departments
        ]
    }


# ============================================================
# SEARCH STUDENTS
# ============================================================

@app.get("/search")
def search_students(
    name: Optional[str] = None,
    email: Optional[str] = None
):

    if not name and not email:

        raise HTTPException(
            status_code=400,
            detail="Provide name or email to search."
        )

    connection = get_connection()

    cursor = connection.cursor()

    if name:

        cursor.execute(
            """
            SELECT * FROM students
            WHERE name LIKE ?
            ORDER BY name
            """,
            (f"%{name}%",)
        )

    else:

        cursor.execute(
            """
            SELECT * FROM students
            WHERE email LIKE ?
            ORDER BY email
            """,
            (f"%{email}%",)
        )

    students = cursor.fetchall()

    connection.close()

    return {
        "count": len(students),
        "students": [
            student_to_dict(student)
            for student in students
        ]
    }


# ============================================================
# DELETE ALL STUDENTS
# ============================================================

@app.delete("/students")
def delete_all_students():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students"
    )

    deleted_count = cursor.rowcount

    connection.commit()

    connection.close()

    return {
        "message": "All student records deleted.",
        "deleted_count": deleted_count
    }


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "                 STUDENT PERFORMANCE API"
    )

    print("=" * 70)

    print(
        "Server: http://127.0.0.1:8000"
    )

    print(
        "Swagger Docs: http://127.0.0.1:8000/docs"
    )

    print(
        "ReDoc: http://127.0.0.1:8000/redoc"
    )

    print("=" * 70)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
