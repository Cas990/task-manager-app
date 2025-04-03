import asyncio
from main import SessionLocal, pwd_context  # Import your async session factory
from models import User

async def create_user():
    async with SessionLocal() as session:  # Use SessionLocal
        async with session.begin():  # Start transaction
            hashed_password = pwd_context.hash("password")  # Hash "password"
            new_user = User(username="testtestuser", hashed_password=hashed_password)
            session.add(new_user)
            await session.commit()  # Commit transaction
            print("User created successfully!")

asyncio.run(create_user())  # Run the async function
