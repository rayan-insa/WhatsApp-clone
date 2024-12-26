import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.conversation import Conversation
from app.models.user import User
from sqlalchemy.orm import joinedload


router = APIRouter()


class ConversationCreate(BaseModel):
    name: str
    user1_id: int
    user2_id: int


class ConversationResponse(BaseModel):
    id: int
    name: str
    user_ids: list[int]


@router.get("/conversations/{user_id}")
async def get_conversations(user_id: int, db: AsyncSession = Depends(get_db)):
    """Fetch all conversations for the current user."""
    try:
        result = await db.execute(
            select(Conversation).filter(
                (Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)
            )
        )
        scalars_result = result.scalars()
        conversations = scalars_result.all()
        return conversations
    except Exception as e:
        logging.error(f"Error fetching conversations: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching conversations: {str(e)}"
        )


@router.get("/conversations")
async def get_all_conversations(db: AsyncSession = Depends(get_db)):
    """Fetch all conversations from the database."""
    try:
        result = await db.execute(select(Conversation))
        conversations = result.scalars().all()
        return conversations
    except Exception as e:
        logging.error(f"Error fetching conversations: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching conversations: {str(e)}"
        )


@router.post("/conversations")
async def create_conversation(
    conversation_data: ConversationCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new conversation."""
    try:
        target_user = await db.execute(
            select(User).filter(User.id == conversation_data.user2_id)
        )
        target_user = target_user.scalar_one()
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Error finding the user : {str(e)}"
        )

    # Check if a conversation already exists between the two users
    existing_conversation = await db.execute(
        select(Conversation).filter(
            (
                (Conversation.user1_id == conversation_data.user1_id)
                & (Conversation.user2_id == conversation_data.user2_id)
            )
            | (
                (Conversation.user1_id == conversation_data.user2_id)
                & (Conversation.user2_id == conversation_data.user1_id)
            )
        )
    )
    if existing_conversation.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Conversation with this user already exists"
        )

    new_conversation = Conversation(
        name=conversation_data.name,
        user1_id=conversation_data.user1_id,
        user2_id=conversation_data.user2_id,
    )
    db.add(new_conversation)
    await db.commit()
    await db.refresh(new_conversation)

    return ConversationResponse(
        id=new_conversation.id,
        name=new_conversation.name,
        user_ids=[new_conversation.user1_id, new_conversation.user2_id],
    )

# for debug
@router.get("/print_conversations") 
async def print_conversations(db: AsyncSession = Depends(get_db)):
    try:
        # Fetch all conversations from the database
        result = await db.execute(select(Conversation))
        conversations = result.scalars().all()

        # Print conversations to the console
        for conversation in conversations:
            print(
                f"Conversation ID: {conversation.id}, Name: {conversation.name}, Users: {conversation.user1_id}, {conversation.user2_id}"
            )

        return {"message": "Conversations printed in the backend console"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching conversations: {str(e)}"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int, db: AsyncSession = Depends(get_db)):
    conversation = await db.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await db.delete(conversation)
    await db.commit()
    return {"message": "Conversation deleted successfully"}
