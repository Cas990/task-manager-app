from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from fastapi import status # type: ignore
from schemas import TokenResponse # type: ignore
from auth import create_access_token, authenticate_user
from db import get_db
from crud import create
from main import app

@app.post("/token", response_model = TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}