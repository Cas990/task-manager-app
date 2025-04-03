from fastapi import FastAPI, Depends, HTTPException, status # type: ignore
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from sqlalchemy.future import select # type: ignore
from sqlalchemy.exc import NoResultFound # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Optional
from models import Task, Base, User
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from passlib.context import CryptContext # type: ignore
import jwt # type: ignore
import datetime

DATABASE_URL = "postgresql+asyncpg://postgres:wWD;\kxe;uYgo7{@localhost:5432/taskdb"

# Create a database engine
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

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

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

tasks = []

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributed = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

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

# USERNAME FUNCTIONS
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar()

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + (expires_delta or datetime.timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user = await get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/register/", response_model = UserResponse)
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

@app.post("/token", response_model = TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# TASK FUNCTIONS
# Create a task
@app.post("/tasks/", response_model = TaskResponse)

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
@app.get("/tasks/", response_model = List[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    return await result.scalars().all()

# Get a specific task by ID
@app.get("/tasks/{task_id}", response_model = TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not accessible")

    return task

# Update a task
@app.put("/tasks/{task_id}", response_model = TaskResponse)
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
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not accessible")

    await db.delete(task)
    await db.commit()

    return {"message": "Task deleted successfully"}