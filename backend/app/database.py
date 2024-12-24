from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

# Get password from the .env file
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")

DATABASE_URL = f"mysql+asyncmy://root:{MYSQLPASSWORD}@localhost:3306/messagely"

# Create the async database engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured async "Session" class
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

# Base class for models
Base = declarative_base()

# Dependency to get async DB session
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
