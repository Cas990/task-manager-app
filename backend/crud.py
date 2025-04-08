from sqlalchemy.ext.asyncio import AsyncSession # type: ignore 
from sqlalchemy.future import select # type: ignore
from models import User, Task
from passlib.context import CryptContext # type: ignore
from schemas import UserCreate, UserResponse, TaskCreate, TaskResponse # type: ignore
from fastapi import Depends, HTTPException, APIRouter # type: ignore
from auth import get_current_user, get_user_by_username
from security import pwd_context
from db import get_db
from typing import List

router = APIRouter()

# USERNAME FUNCTIONS

@router.post("/register/", response_model = UserResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# TASK FUNCTIONS
# Create a task
@router.post("/tasks/", response_model = TaskResponse)

async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = Task(title=task.title, description=task.description, completed=task.completed, user_id=current_user.id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task
    # task.id = len(tasks) + 1  # Auto-generate ID based on list length
    # tasks.append(task)
    # return task

# Get all tasks
@router.get("/tasks/", response_model = List[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    tasks = result.scalars().all()
    return tasks

# Get a specific task by ID
@router.get("/tasks/{task_id}", response_model = TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not accessible")

    return task

# Update a task
@router.put("/tasks/{task_id}", response_model = TaskResponse)
async def update_task(task_id: int, task_update: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not accessible")

    # Update fields
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed

    await db.commit()
    await db.refresh(task) # Refresh object with new data from DB

    return task

# Delete a task
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not accessible")

    await db.delete(task)
    await db.commit()

    return {"message": "Task deleted successfully"}