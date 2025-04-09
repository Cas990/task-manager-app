# Task Manager App

Simple task manager app built with Vue.js (frontend), FastAPI (backend), and PostgreSQL (database).
This project serves as a learning exercise to understand the integration of these technologies.

## Features
- **User authentication** using FastAPI and JWT tokens.
- **Task Management**: Create, update, and delete user-specific tasks.
- **Persistent Storage**: Task and user data are stored in a PostgreSQL database.

## Prerequisites
To run this app, you need to have the following installed:
- **Python 3.9+**
- **Node.js 18+** (for Vue.js frontend)
- **PostgreSQL 13+** (for database)
- **pip and virtualenv** (for backend dependencies)

## Setup instructions

### Backend Setup

# Navigate to the backend directory 
cd backend

# Create a virtual environment (if you haven't already)
python -m venv venv
# Or: python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt


### Frontend Setup
# Navigate to the frontend directory
cd frontend

# Install frontend dependencies (see `package.json`)
npm install

# Run the development server
npm run dev

### Running the app
Start both the backend and frontend in separate terminals.

## Start backend
# Navigate to the backend directory
cd backend

# Run the backend
uvicorn main:app --reload

Accessible in the browser at http://localhost:8000

## Start frontend
# Navigate to the frontend directory
cd frontend

# Run the frontend
npm run dev

Accessible in the browser at http://localhost:5173

### Environment Variables
Create a `.env` file in the backend directory and add the following environment variables (replace with your own credentials):

DATABASE_URL=postgresql://user:password@localhost:5432/database_name
SECRET_KEY=your_secret_key

### Notes
- Make sure to initialize the database before running the app by running db_init.py using the following command:
    python backend/db_init.py
- An `alembic` directory is used for database migrations.