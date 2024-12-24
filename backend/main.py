from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import Base, async_engine, get_db
from app.routes import user_routes, message_routes
from app.models.user import User
from app.models.conversation import Conversation
from app.models.groupchat import GroupChat
from app.models.message import Message
from app.routes import groupchat_routes
from app.routes import db_routes
from app.routes import conversation_routes
import threading
from app.kafka.kafka_consumer import *


app = FastAPI()


def run_kafka_consumer():
    consume_messages()


# Run the consumer in a separate thread
threading.Thread(target=run_kafka_consumer, daemon=True).start()


# Async function to create tables
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Run the table creation at startup
@app.on_event("startup")
async def startup():
    await create_tables()


# Include routers
app.include_router(user_routes.router)
app.include_router(message_routes.router)
app.include_router(groupchat_routes.router)
app.include_router(db_routes.router)
app.include_router(conversation_routes.router)


@app.get("/")
def read_root():
    return {"message": "Backend is running!"}
