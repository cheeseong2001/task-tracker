from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from datetime import datetime
from . import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield

app = FastAPI(lifespan=lifespan)

class TaskCreate(BaseModel):
    task_name: str
    description: str | None = ""
    # due_date: datetime | None = None  # TODO: Implement timestamp 

class Task(TaskCreate):
    id: int

@app.post("/tasks/add")
def add_task(new_task: TaskCreate) -> Task:
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, description) VALUES (%s, %s) RETURNING id;", (new_task.task_name, new_task.description))
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(500, "Failed to insert task")
    task_id = result[0]

    conn.commit()
    cursor.close()

    task_obj = Task(id=task_id, **new_task.model_dump())
    return task_obj

@app.get("/tasks/{task_id}")
def get_task_details(task_id: int) -> Task:
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(404, f"Task with id {task_id} not found")
    task_obj = Task(id=row[0], task_name=row[1], description=row[2])

    return task_obj

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    if cursor.rowcount == 0:
        raise HTTPException(404, f"Task with id {task_id} not found")
    conn.commit()
    return {"success": True}

@app.get("/tasks")
def get_all_tasks() -> list[Task]:
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id ASC;")
    rows = cursor.fetchall()

    return [Task(id=row[0], task_name=row[1], description=row[2]) for row in rows]