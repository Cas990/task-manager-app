from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

tasks = []

# Task model
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# Create a task
@app.post("/tasks/")

def create_task(task: Task):
    tasks.append(task)
    return task

# Get all tasks
@app.get("/tasks/", response_model = List[Task])
def get_tasks():
    return tasks

# Get a specific task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return {"error": "Task not found"}

# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    return {"error": "Task not found"}

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Task deleted successfully"}