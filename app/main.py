from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.schemas import TaskCreate, TaskUpdate

app = FastAPI(
    title="Task API",
    description="API для работы с задачами, написанное с FastAPI",
    version="0.1.0",
)

TASKS: list[dict] = []
STUDENTS: list[dict] = []

@app.get("/")
def root():
    return {"message": "Hello, WORLD!"}

# --- Эндпоинты для задач (были изначально) ---

@app.get("/tasks")
def get_tasks():
    return TASKS

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = {"id": len(TASKS) + 1, **task.model_dump()}
    TASKS.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task_patch: TaskUpdate):
    for task in TASKS:
        if task["id"] == task_id:
            updates = task_patch.model_dump(exclude_unset=True)
            task.update(updates)
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            TASKS.remove(task)
            return TASKS
    raise HTTPException(status_code=404, detail="Задача не найдена")

@app.get("/search")
def search_tasks(q: str="", limit: int=10):
    result = []
    for task in TASKS:
        if task["title"].find(q) != -1:
            result.append(task)
    return result

# Эндпоинты для студентов

class Student(BaseModel):
    first_name: str
    last_name: str
    group: str
    age: int

@app.post("/students/", status_code=201)
def create_student(student: Student):
    STUDENTS.append(student)
    return {"message": "Студент добавлен", "student": student}

@app.get("/students/{student_name}")
def get_student(student_name: str):
    for student in STUDENTS:
        if student.first_name.lower() == student_name.lower() or student.last_name.lower() == student_name.lower():
            return student
    raise HTTPException(status_code=404, detail="Студент не найден")