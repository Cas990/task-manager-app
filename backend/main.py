from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from auth import router as auth_router
from crud import router as crud_router


app = FastAPI()

origins = [
    "http://localhost:5173",
]

methods = [
    "GET",
    "POST",
    "PUT",
    "DELETE"
]

headers = ["Content-Type", "Authorization"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows frontend origin
    allow_credentials=True,
    allow_methods=methods,  # Allows necessary HTTP methods
    allow_headers=headers,  # Allows necessary headers
)

app.include_router(auth_router)
app.include_router(crud_router)

