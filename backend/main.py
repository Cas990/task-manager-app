from fastapi import FastAPI, Depends, HTTPException # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine # type: ignore
from sqlalchemy.orm import sessionmaker, declarative_base # type: ignore
from sqlalchemy.future import select # type: ignore
from sqlalchemy.exc import NoResultFound # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Optional
from models import Task
from fastapi.middleware.cors import CORSMiddleware # type: ignore

DATABASE_URL = "postgresql+asyncpg://postgres:wWD;\kxe;uYgo7{@localhost:5432/taskdb"

# Create a database engine
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

app = FastAPI()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

tasks = []

# Task model
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    class Config:
        from_attributed = True # Enable conversion from SQLAlchemy models

# Create a task
@app.post("/tasks/", response_model = TaskCreate)

async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description, completed=task.completed)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task
    # task.id = len(tasks) + 1  # Auto-generate ID based on list length
    # tasks.append(task)
    # return task

# Get all tasks
@app.get("/tasks/", response_model = List[TaskCreate])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    return await Task.get_all(db)

# Get a specific task by ID
@app.get("/tasks/{task_id}", response_model = TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
    # for task in tasks:
    #     if task.id == task_id:
    #         return task
    # return {"error": "Task not found"}

# Update a task
@app.put("/tasks/{task_id}", response_model = TaskResponse)
async def update_task(task_id: int, task_update: TaskCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed

    await db.commit()
    await db.refresh(task) # Refresh object with new data from DB

    return task
    # for i, task in enumerate(tasks):
    #     if task.id == task_id:
    #         tasks[i] = updated_task
    #         return updated_task
    # return {"error": "Task not found"}

# Delete a task
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    # global tasks
    # tasks = [task for task in tasks if task.id != task_id]
    return {"message": "Task deleted successfully"}