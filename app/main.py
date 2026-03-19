from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Task Tracker API")

# In-memory "database"
tasks = {}
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Tracker API!"}

@app.get("/tasks")
def get_tasks(completed: Optional[bool] = None):
    if completed is None:
        return list(tasks.values())
    return [task for task in tasks.values() if task["completed"] == completed]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/tasks")
def create_task(task: Task):
    global task_id_counter
    tasks[task_id_counter] = {"id": task_id_counter, **task.dict()}
    task_id_counter += 1
    return tasks[task_id_counter - 1]

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = {"id": task_id, **update_task.dict()}
    return tasks[task_id]

@app.delete("tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": "Task deleted"}