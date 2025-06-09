from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models import *
from ..enums import StatusEnum
from .. import db
from psycopg2 import sql

router = APIRouter()

@router.post("/tasks/add")
def add_task(new_task: TaskCreate) -> Task:
    with db.get_db_cursor() as cursor:
        cursor.execute("INSERT INTO tasks (task_name, description, status) VALUES (%s, %s, %s) RETURNING *;", 
                    (new_task.task_name, new_task.description, StatusEnum.todo))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(500, "Failed to insert task")

        columns = [desc[0] for desc in cursor.description] # type: ignore
        task_dict = dict(zip(columns, row))
        return Task(**task_dict)

@router.get("/tasks/{task_id}")
def get_task_details(task_id: int) -> Task:
    with db.get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(404, f"Task with id {task_id} not found")
        
        columns = [desc[0] for desc in cursor.description] # type: ignore
        task_dict = dict(zip(columns, row))
        return Task(**task_dict)
    
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict:
    with db.get_db_cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(404, f"Task with id {task_id} not found")
        return {"success": True}

@router.get("/tasks")
def get_all_tasks() -> list[Task]:
    with db.get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM tasks ORDER BY id ASC;")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] # type: ignore
        tasks = [dict(zip(columns, row)) for row in rows]
        return [Task(**task) for task in tasks]

@router.patch("/tasks/{task_id}/status")
def update_status(task_id: int, status_update: StatusUpdate) -> Task:
    with db.get_db_cursor() as cursor:
        cursor.execute("UPDATE tasks SET status = %s WHERE id = %s RETURNING *;", (status_update.new_status, task_id))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(404, f"Task with id {task_id} not found")
        
        columns = [desc[0] for desc in cursor.description] # type: ignore
        task_dict = dict(zip(columns, row))
        return Task(**task_dict)

@router.patch("/tasks/{task_id}/edit")
def edit_task(task_id: int, task_update: TaskEdit) -> Task:
    with db.get_db_cursor() as cursor:
        data = task_update.model_dump(exclude_unset=True)
        if data == {}:
            raise HTTPException(400, "No fields provided for update")
        
        columns = [sql.Identifier(k) for k in data.keys()]
        placeholders = [sql.Placeholder() for _ in data]
        assignments = [sql.SQL("{} = {}").format(col, ph) for col, ph in zip(columns, placeholders)]

        query = sql.SQL("UPDATE tasks SET {assignments} WHERE id = %s RETURNING *").format(
            assignments=sql.SQL(", ").join(assignments)
        )

        cursor.execute(query, list(data.values()) + [task_id])
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(404, f"Task with id {task_id} not found")

        columns = [desc[0] for desc in cursor.description] # type: ignore
        task_dict = dict(zip(columns, row))

        return Task(**task_dict)
    