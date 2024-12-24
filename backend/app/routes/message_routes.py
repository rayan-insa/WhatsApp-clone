from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.message import Message
from app.database import get_db
from pydantic import BaseModel
from typing import List

from app.models.user import User
from app.kafka.kafka_utils import *


class MessageCreate(BaseModel):
    sender_id: int
    conversation_id: int
    groupchat_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    content: str
    sender_id: int
    conversation_id: int
    groupchat_id: int
    sender_username: str

    class Config:
        orm_mode = True

router = APIRouter()


@router.post("/messages/conversation", response_model=MessageResponse)
async def create_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    new_message = Message(
        content=message.content,
        sender_id=message.sender_id,
        conversation_id=message.conversation_id,
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    senderID = new_message.sender_id
    sender = await db.get(User, senderID)
    await db.refresh(sender)
    
    # Prepare the message data to be sent to Kafka
    message_data = {
        "sender_id": new_message.sender_id,
        "content": new_message.content,
        "conversation_id": new_message.conversation_id,
        "sender_username": sender.username,
        "groupchat_id": message.groupchat_id,
    }

    # Send the message to Kafka
    send_message_to_kafka(message_data)
    return MessageResponse(
        id=new_message.id,
        content=new_message.content,
        sender_id=new_message.sender_id,
        conversation_id=new_message.conversation_id,
        sender_username=new_message.sender.username,
        groupchat_id=0,
    )


@router.post("/messages/groupchat", response_model=MessageResponse)
async def create_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    new_message = Message(
        content=message.content,
        sender_id=message.sender_id,
        groupchat_id=message.groupchat_id,
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    senderID = new_message.sender_id
    sender = await db.get(User, senderID)
    await db.refresh(sender)

    return MessageResponse(
        id=new_message.id,
        content=new_message.content,
        sender_id=new_message.sender_id,
        groupchat_id=new_message.groupchat_id,
        sender_username=new_message.sender.username,
        conversation_id=0,
    )


@router.get(
    "/messages/conversation/{conversation_id}", response_model=List[MessageResponse]
)
async def get_conversation_messages(
    conversation_id: int, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Message)
        .options(joinedload(Message.sender))
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp)
    )
    messages = result.scalars().all()

    response = [
        MessageResponse(
            id=msg.id,
            content=msg.content,
            sender_id=msg.sender_id,
            conversation_id=msg.conversation_id,
            sender_username=msg.sender.username,
            groupchat_id=0,
        )
        for msg in messages
    ]

    return response


@router.get("/messages/groupchat/{groupchat_id}", response_model=List[MessageResponse])
async def get_groupchat_messages(groupchat_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Message)
        .options(joinedload(Message.sender))
        .filter(Message.groupchat_id == groupchat_id)
        .order_by(Message.timestamp)
    )
    messages = result.scalars().all()

    response = [
        MessageResponse(
            id=msg.id,
            content=msg.content,
            sender_id=msg.sender_id,
            groupchat_id=msg.groupchat_id,
            sender_username=msg.sender.username,
            conversation_id=0,
        )
        for msg in messages
    ]

    return response
