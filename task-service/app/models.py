from pydantic import BaseModel
from . import enums

class TaskCreate(BaseModel):
    task_name: str
    description: str | None = ""
    # due_date: datetime | None = None  # TODO: Implement timestamp 

class Task(TaskCreate):
    id: int
    status: enums.StatusEnum

class StatusUpdate(BaseModel):
    new_status: enums.StatusEnum

class TaskEdit(BaseModel, extra="forbid"):
    task_name: str | None = None
    description: str | None = None