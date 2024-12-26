from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_engine
from app.database import Base, get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.models.message import Message
from app.models.groupchat import GroupChat
from sqlalchemy.future import select
import logging
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/db_test")
async def db_test():
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT DATABASE();"))
            return {"database": result.scalar()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to the database: {str(e)}"
        )


@router.get("/reset_db")
async def reset_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(
            text(
                "DROP TABLE IF EXISTS messages, conversations, group_members, groupchats, users CASCADE"
            )
        )
        await db.execute(text("DROP TABLE IF EXISTS alembic_version"))
        await db.commit()

        # Recreate tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error resetting the database: {str(e)}"
        )


@router.get("/add_test_data")
async def add_test_data(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(
            text(
                "DROP TABLE IF EXISTS messages, conversations, group_members, groupchats, users CASCADE"
            )
        )
        await db.execute(text("DROP TABLE IF EXISTS alembic_version"))
        await db.commit()

        # Recreate tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Create users
        users = [
            User(username="alice", email="alice@example.com"),
            User(username="bob", email="bob@example.com"),
            User(username="charlie", email="charlie@example.com"),
            User(username="diana", email="diana@example.com"),
            User(username="edward", email="edward@example.com"),
            User(username="fiona", email="fiona@example.com"),
            User(username="george", email="george@example.com"),
            User(username="hannah", email="hannah@example.com"),
            User(username="ivan", email="ivan@example.com"),
            User(username="julia", email="julia@example.com"),
        ]

        db.add_all(users)
        await db.commit()

        for user in users:
            await db.refresh(user)

        # Create conversations
        conversations = [
            Conversation(user1_id=users[0].id, user2_id=users[1].id),
            Conversation(user1_id=users[2].id, user2_id=users[3].id),
            Conversation(user1_id=users[5].id, user2_id=users[6].id),
            Conversation(user1_id=users[7].id, user2_id=users[8].id),
        ]

        db.add_all(conversations)
        await db.commit()

        for conversation in conversations:
            await db.refresh(conversation)

        for user in users:
            await db.refresh(user)

        # Create messages for conversations
        conversation_messages = [
            Message(
                conversation=conversations[0],
                sender_id=users[0].id,
                content="Hi Bob, how are you?",
            ),
            Message(
                conversation=conversations[0],
                sender_id=users[1].id,
                content="I'm good, Alice! How about you?",
            ),
            Message(
                conversation=conversations[1],
                sender_id=users[2].id,
                content="Hey Diana, did you finish the report?",
            ),
            Message(
                conversation=conversations[1],
                sender_id=users[3].id,
                content="Yes, Charlie. Sending it now.",
            ),
            Message(
                conversation=conversations[2],
                sender_id=users[5].id,
                content="George, ready for the meeting?",
            ),
            Message(
                conversation=conversations[2],
                sender_id=users[6].id,
                content="Absolutely, Fiona. Let's nail this!",
            ),
            Message(
                conversation=conversations[3],
                sender_id=users[7].id,
                content="Ivan, can you review my code?",
            ),
            Message(
                conversation=conversations[3],
                sender_id=users[8].id,
                content="Sure, Hannah. Send it over.",
            ),
        ]

        db.add_all(conversation_messages)
        await db.commit()

        for user in users:
            await db.refresh(user)

        # Create groupchats
        groupchats = [
            GroupChat(name="Project Team A", admin_id=users[0].id),
            GroupChat(name="Weekend Hikers", admin_id=users[3].id),
            GroupChat(name="Music Lovers", admin_id=users[6].id),
        ]

        groupchats[0].members.extend([users[0], users[1], users[2], users[3]])
        groupchats[1].members.extend([users[3], users[4], users[5], users[6]])
        groupchats[2].members.extend([users[6], users[7], users[8], users[9]])

        db.add_all(groupchats)
        await db.commit()

        for groupchat in groupchats:
            await db.refresh(groupchat)

        for user in users:
            await db.refresh(user)

        # Create messages for groupchats
        group_messages = [
            Message(
                groupchat=groupchats[0],
                sender_id=users[0].id,
                content="Team, let's sync up tomorrow at 10 AM.",
            ),
            Message(
                groupchat=groupchats[0],
                sender_id=users[2].id,
                content="Got it, Alice. See you then.",
            ),
            Message(
                groupchat=groupchats[1],
                sender_id=users[4].id,
                content="Who's up for a hike this Saturday?",
            ),
            Message(
                groupchat=groupchats[1],
                sender_id=users[5].id,
                content="Count me in, Diana!",
            ),
            Message(
                groupchat=groupchats[2],
                sender_id=users[7].id,
                content="Check out this new song I found!",
            ),
            Message(
                groupchat=groupchats[2],
                sender_id=users[9].id,
                content="Awesome, Julia! Sharing my playlist too.",
            ),
        ]

        db.add_all(group_messages)
        await db.commit()

        return {"message": "Demo-friendly test data added successfully"}
    except Exception as e:
        print(f"Error adding test data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding test data: {str(e)}")
