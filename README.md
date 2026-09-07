# 🎓 Student Performance API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python">
  <img src="https://img.shields.io/badge/FastAPI-REST%20API-green?logo=fastapi">
  <img src="https://img.shields.io/badge/Database-SQLite-orange?logo=sqlite">
  <img src="https://img.shields.io/badge/Validation-Pydantic-red">
  <img src="https://img.shields.io/badge/Status-Completed-success">
</p>

<p align="center">
  <b>A Python-based REST API for managing student academic records, calculating GPA, analyzing performance, filtering students, generating statistics, and providing personalized academic recommendations.</b>
</p>

---

## 📌 Overview

**Student Performance API** is a backend application built with **Python and FastAPI** that provides RESTful endpoints for managing student academic information.

The application stores student records in a **SQLite database** and automatically calculates GPA, evaluates academic performance, analyzes attendance, and generates recommendations.

The API provides:

* 👨‍🎓 Student management
* 📚 Academic record management
* 📊 GPA calculation
* 📈 Performance analysis
* 🔎 Student search
* 🏆 Top-performer identification
* 📋 Department statistics
* ✅ Input validation
* 🗄️ SQLite database integration
* 📖 Interactive Swagger API documentation
* 💡 Automated academic recommendations

---

## ✨ Features

### 👨‍🎓 Student Management

The API supports complete student CRUD operations:

* Create students
* View all students
* View individual students
* Update student information
* Delete students
* Delete all student records

### 📊 GPA Calculation

The application automatically converts marks into a GPA value.

|    Marks |  GPA |
| -------: | ---: |
|   90–100 | 10.0 |
|    80–89 |  9.0 |
|    70–79 |  8.0 |
|    60–69 |  7.0 |
|    50–59 |  6.0 |
|    40–49 |  5.0 |
| Below 40 |  0.0 |

> The GPA mapping is a project-defined calculation and is not intended to represent a specific university grading regulation.

### 📈 Performance Analysis

The API categorizes student performance as:

* 🟢 Outstanding
* 🔵 Excellent
* 🟡 Good
* 🟠 Average
* 🔴 Needs Improvement

Performance is evaluated using marks and attendance.

### 💡 Academic Recommendations

The system automatically generates recommendations based on:

* Academic marks
* Attendance percentage
* Overall performance

Example:

```text
Focus on improving academic performance.
Improve attendance to meet the recommended level.
```

### 🔎 Student Search

Students can be searched using:

* Name
* Email

Example:

```text
/search?name=Aakash
```

### 🏆 Top Performers

The API can return the highest-performing students based on marks.

Example:

```text
/students/top-performers?limit=5
```

### 📊 Statistics

The statistics endpoint provides:

* Total students
* Average marks
* Average attendance
* Highest marks
* Lowest marks
* Department-wise student count
* Department-wise average marks

### 🔍 Filtering

Students can be filtered by:

* Department
* Academic year
* Minimum marks

Example:

```text
/students?department=IT&year=2&min_marks=70
```

### 📖 Interactive API Documentation

FastAPI automatically provides interactive API documentation through:

```text
/docs
```

and:

```text
/redoc
```

Users can test API endpoints directly from the browser.

---

## 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core programming language |
| FastAPI    | REST API framework        |
| Uvicorn    | ASGI server               |
| SQLite     | Database                  |
| Pydantic   | Data validation           |
| SQL        | Database queries          |
| Git        | Version control           |
| GitHub     | Project hosting           |

---

## 📂 Project Structure

This project is intentionally designed as a **single Python file**.

```text
student-performance-api/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

The SQLite database is automatically created when the application starts:

```text
students.db
```

> `students.db` should normally be included in `.gitignore` because it is generated locally.

---

## 🚀 Getting Started

### Prerequisites

Make sure **Python 3.x** is installed.

Check your Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

---

## 📥 Installation

Clone the repository:

```bash
git clone https://github.com/aakashp2008/student-performance-api.git
```

Navigate to the project directory:

```bash
cd student-performance-api
```

Install the required packages:

```bash
pip install fastapi uvicorn
```

---

## ▶️ Run the Application

Start the API server:

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

## 📖 API Documentation

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

This opens the **Swagger UI**, where you can test all API endpoints interactively.

FastAPI also provides ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 🏠 API Endpoints

| Method | Endpoint                     | Description         |
| ------ | ---------------------------- | ------------------- |
| GET    | `/`                          | API information     |
| GET    | `/health`                    | Health check        |
| POST   | `/students`                  | Create student      |
| GET    | `/students`                  | Get all students    |
| GET    | `/students/{id}`             | Get student by ID   |
| PUT    | `/students/{id}`             | Update student      |
| DELETE | `/students/{id}`             | Delete student      |
| GET    | `/students/{id}/performance` | Analyze performance |
| GET    | `/students/top-performers`   | Get top performers  |
| GET    | `/statistics`                | Get statistics      |
| GET    | `/search`                    | Search students     |
| DELETE | `/students`                  | Delete all students |

---

## ➕ Create Student

### Endpoint

```text
POST /students
```

### Example Request

```json
{
  "name": "Aakash P",
  "email": "aakash@example.com",
  "department": "IT",
  "year": 2,
  "marks": 88,
  "attendance": 92
}
```

### Example Response

```json
{
  "message": "Student created successfully",
  "student": {
    "id": 1,
    "name": "Aakash P",
    "email": "aakash@example.com",
    "department": "IT",
    "year": 2,
    "marks": 88.0,
    "attendance": 92.0,
    "gpa": 9.0,
    "performance_level": "Excellent",
    "recommendations": [
      "Excellent academic performance. Keep progressing.",
      "Good attendance. Maintain consistency."
    ]
  }
}
```

---

## 📋 Get All Students

### Endpoint

```text
GET /students
```

Example:

```text
GET /students
```

The API returns all stored student records.

---

## 🔎 Filter Students

Students can be filtered using query parameters.

### Department

```text
GET /students?department=IT
```

### Academic Year

```text
GET /students?year=2
```

### Minimum Marks

```text
GET /students?min_marks=80
```

### Combined Filters

```text
GET /students?department=IT&year=2&min_marks=80
```

---

## 👤 Get Student by ID

### Endpoint

```text
GET /students/{student_id}
```

Example:

```text
GET /students/1
```

---

## ✏️ Update Student

### Endpoint

```text
PUT /students/{student_id}
```

Example:

```json
{
  "marks": 92,
  "attendance": 95
}
```

The API automatically recalculates the student's GPA and performance level.

---

## 🗑️ Delete Student

### Endpoint

```text
DELETE /students/{student_id}
```

Example:

```text
DELETE /students/1
```

---

## 📈 Performance Analysis

### Endpoint

```text
GET /students/{student_id}/performance
```

Example:

```text
GET /students/1/performance
```

Example response:

```json
{
  "student_id": 1,
  "student_name": "Aakash P",
  "academic_performance": {
    "marks": 88.0,
    "gpa": 9.0,
    "performance_level": "Excellent"
  },
  "attendance": {
    "percentage": 92.0,
    "status": "Good"
  },
  "recommendations": [
    "Excellent academic performance. Keep progressing.",
    "Good attendance. Maintain consistency."
  ]
}
```

---

## 🏆 Top Performers

### Endpoint

```text
GET /students/top-performers
```

Specify the number of students:

```text
GET /students/top-performers?limit=5
```

The API returns students ordered by marks in descending order.

---

## 📊 Statistics

### Endpoint

```text
GET /statistics
```

The endpoint provides overall statistics such as:

```text
Total Students
Average Marks
Average Attendance
Highest Marks
Lowest Marks
```

It also provides department-wise statistics:

```text
Department
Student Count
Average Marks
```

---

## 🔍 Search

### Search by Name

```text
GET /search?name=Aakash
```

### Search by Email

```text
GET /search?email=aakash@example.com
```

The search returns matching student records.

---

## 🗄️ Database

The project uses **SQLite** for local data storage.

The database is automatically created:

```text
students.db
```

### Student Table

The database stores:

```text
id
name
email
department
year
marks
attendance
```

Additional values such as GPA and performance level are calculated dynamically rather than permanently stored.

---

## 🔄 Application Workflow

```text
                 ┌─────────────────────┐
                 │      API Client      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      FastAPI        │
                 └──────────┬──────────┘
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
          ┌──────────────┐    ┌──────────────┐
          │  Validation  │    │ API Routing  │
          │  Pydantic    │    │              │
          └──────┬───────┘    └──────┬───────┘
                 │                   │
                 └─────────┬─────────┘
                           ▼
                 ┌─────────────────────┐
                 │   SQLite Database   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Performance Engine  │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           GPA         Performance   Recommendations
        Calculation      Analysis
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                 ┌─────────────────────┐
                 │     JSON Response   │
                 └─────────────────────┘
```

---

## 🧠 GPA Calculation Logic

The application uses a simple rule-based marks-to-GPA conversion.

Example:

```text
Marks = 88

88 falls between 80 and 89

GPA = 9.0
```

Another example:

```text
Marks = 72

72 falls between 70 and 79

GPA = 8.0
```

---

## 📊 Performance Logic

Performance depends on both marks and attendance.

Example:

```text
Marks      = 92
Attendance = 94%

Performance = Outstanding
```

Another example:

```text
Marks      = 55
Attendance = 70%

Performance = Average
```

---

## 💡 Recommendation System

The application generates recommendations based on academic performance.

### Low Marks

```text
Focus on improving academic performance.
```

### Moderate Marks

```text
Increase study consistency to improve marks.
```

### High Marks

```text
Excellent academic performance. Keep progressing.
```

### Low Attendance

```text
Improve attendance to meet the recommended level.
```

### Good Attendance

```text
Good attendance. Maintain consistency.
```

---

## ✅ Input Validation

Pydantic validates incoming student data.

Examples of validation rules:

```text
Name:
Minimum 2 characters

Year:
1–5

Marks:
0–100

Attendance:
0–100

Email:
Required and unique
```

Invalid data is rejected automatically by FastAPI/Pydantic.

---

## 🛡️ Error Handling

The API handles common errors including:

* Student not found
* Duplicate email
* Invalid input
* Empty update requests
* Invalid search requests
* Invalid student IDs

Example:

```json
{
  "detail": "Student not found."
}
```

---

## 🔐 Security

The current version is designed as a local educational backend.

It does **not** include:

* User authentication
* JWT authorization
* Password management
* Role-based access control

These can be added in future versions.

> Do not use this version for storing sensitive student information in a production environment without appropriate authentication, authorization, encryption, and privacy controls.

---

## 🧩 Concepts Demonstrated

This project demonstrates practical knowledge of:

* Python programming
* FastAPI
* REST API development
* HTTP methods
* CRUD operations
* SQLite
* SQL queries
* Pydantic validation
* JSON
* Query parameters
* Path parameters
* Exception handling
* API routing
* Database operations
* Data processing
* Rule-based analysis
* Backend development

---

## 🎯 Project Objectives

The main objectives are:

1. Build a RESTful backend using FastAPI.
2. Learn API endpoint design.
3. Implement CRUD operations.
4. Work with SQLite databases.
5. Validate API input using Pydantic.
6. Calculate GPA programmatically.
7. Analyze student performance.
8. Generate automated recommendations.
9. Implement search and filtering.
10. Create statistical API endpoints.
11. Practice backend error handling.
12. Use interactive API documentation.

---

## 🎓 Learning Outcomes

Through this project, the developer gains experience in:

* Building REST APIs
* Working with FastAPI
* Creating database-backed applications
* Writing SQL queries
* Designing CRUD endpoints
* Validating API requests
* Returning structured JSON responses
* Handling API errors
* Building reusable Python functions
* Developing backend applications
* Working with Swagger/OpenAPI documentation

---

## ⚠️ Limitations

The current version has some limitations:

* Uses a simple marks-to-GPA conversion.
* Uses SQLite for local storage.
* Does not have authentication.
* Does not have authorization.
* Does not support multiple users/accounts.
* Does not include a frontend.
* Does not include advanced analytics.
* Does not use a production database.
* Does not include automated tests.
* Performance recommendations are rule-based.

Therefore, this project should be considered a **learning and portfolio backend application**, rather than a production-ready student management system.

---

## 🚀 Future Enhancements

### 🔐 1. JWT Authentication

Add secure authentication using:

```text
JWT
OAuth2
Password Hashing
```

### 👥 2. Role-Based Access

Support different users:

```text
Admin
Faculty
Student
```

### 📊 3. Analytics Dashboard

Create a frontend dashboard showing:

* Average marks
* GPA distribution
* Attendance trends
* Department comparison
* Top performers

### 🌐 4. Frontend Application

Build a frontend using:

```text
HTML
CSS
JavaScript
React
```

### 🗄️ 5. PostgreSQL

Replace SQLite with PostgreSQL for production-style database management.

### 🧪 6. Automated Testing

Add:

```text
Pytest
FastAPI TestClient
```

for API testing.

### ☁️ 7. Cloud Deployment

Deploy the API using a cloud platform.

### 📧 8. Notification System

Send notifications when:

* Attendance becomes low
* Performance decreases
* Marks improve
* Academic targets are reached

### 🤖 9. AI Performance Prediction

Use machine-learning models to predict:

* Future academic performance
* Risk of low performance
* Attendance-related risk
* Improvement probability

### 📱 10. Mobile Application

Connect the backend with a Flutter mobile application for students and faculty.

---

## 💼 Why This Project?

This project goes beyond a basic Python application by combining:

```text
Python
   +
FastAPI
   +
REST API
   +
SQLite
   +
SQL
   +
Pydantic
   +
Data Validation
   +
CRUD
   +
Analytics
   +
Real-World Problem Solving
```

It demonstrates skills useful for:

* 💻 Software Engineering internships
* 🌐 Backend Development internships
* 🐍 Python Developer roles
* ⚡ FastAPI projects
* 🗄️ Database-related roles
* 🎓 College projects
* 💼 Placement preparation
* 🧑‍💻 Technical interviews

---

## 📌 Resume Project Description

You can add this project to your resume as:

> **Student Performance API** — Developed a FastAPI-based REST backend with SQLite for managing student academic records, implementing CRUD operations, Pydantic validation, GPA calculation, performance analysis, search/filtering, department statistics, and automated academic recommendations.

---

## 🏆 Key Highlights

```text
✓ FastAPI REST API
✓ SQLite Database
✓ CRUD Operations
✓ Pydantic Validation
✓ GPA Calculation
✓ Performance Analysis
✓ Academic Recommendations
✓ Student Search
✓ Filtering
✓ Top Performer Analysis
✓ Department Statistics
✓ Swagger API Documentation
✓ Error Handling
✓ Backend Development
```

---

## 🧑‍💻 Author

### AAKASH P

**B.Tech Information Technology Student**
**Panimalar Engineering College**

### Technical Skills

```text
Python | Java | C | SQL | DSA | FastAPI | AI/ML | Git | GitHub
```

---

## 🔗 GitHub

### GitHub Profile

https://github.com/aakashp2008

### Project Repository

https://github.com/aakashp2008/student-performance-api

---

## ⭐ Support

If you find this project useful:

⭐ Star the repository
🍴 Fork the repository
🐛 Report issues
💡 Suggest improvements

---

## 📜 License

This project is intended for **educational, learning, and portfolio purposes**.

You are free to modify and extend the project for learning and development.
