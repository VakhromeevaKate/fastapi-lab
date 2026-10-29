from pydantic import BaseModel
from app.schemas import TaskCreate, TaskUpdate
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskOut, TaskUpdate, StudentCreate

app = FastAPI(
    title="Task API",
    description="API для работы с задачами, написанное с FastAPI",
    version="0.2.0"
)

TASKS: list[dict] = []
# Создаём таблицы при старте (для лабораторной; в реальном проекте — Alembic)
Base.metadata.create_all(bind=engine)

STUDENTS: list[dict] = []

@app.get("/")
def root():
    return {"message": "Hello, WORLD!"}

# --- Эндпоинты для задач (были изначально) ---

@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.get("/tasks/search", response_model=list[TaskOut])
def search_tasks(
    q: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    return db.query(Task).filter(Task.title.ilike(f"%{q}%")).order_by(Task.id).all()

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, patch: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    updates = patch.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

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
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(task_id, db)
    db.delete(task)
    db.commit()
    return db.query(Task).all()
