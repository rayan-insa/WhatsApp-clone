import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select    
from sqlalchemy.orm import joinedload, selectinload
from app.models.groupchat import GroupChat, group_members
from app.models.user import User
from app.database import get_db
from pydantic import BaseModel
from sqlalchemy import delete

class GroupChatCreate(BaseModel):
    name: str
    admin_id: int


class AddMemberRequest(BaseModel):
    user_id: int


router = APIRouter()


@router.post("/groupchats")
async def create_groupchat(
    group_chat_data: GroupChatCreate, db: AsyncSession = Depends(get_db)
):
    admin = await db.get(User, group_chat_data.admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found")

    group_chat = GroupChat(name=group_chat_data.name, admin_id=group_chat_data.admin_id)
    db.add(group_chat)
    await db.commit()
    await db.refresh(group_chat)
    return {"message": "Group chat created successfully", "group_chat": group_chat}


@router.post("/groupchats/{group_id}/add_member")
async def add_member_to_groupchat(
    group_id: int,
    add_member_request: AddMemberRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await db.execute(
            select(GroupChat)
            .filter(GroupChat.id == group_id)
            .options(selectinload(GroupChat.members))
        )
        group_chat = result.scalars().first()
        if not group_chat:
            raise HTTPException(status_code=404, detail="Group chat not found")

        user_result = await db.execute(
            select(User).filter(User.id == add_member_request.user_id)
        )
        user = user_result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user in group_chat.members:
            raise HTTPException(
                status_code=400, detail="User already in the group chat"
            )
        group_chat.members.append(user)
        await db.commit()
        await db.refresh(user)
        await db.refresh(group_chat)

        return {
            "message": f"User {user.username} added to group chat {group_chat.name}"
        }
    except Exception as e:
        logging.error(f"Error adding member to group chat: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error adding member to group chat: {str(e)}"
        )


@router.get("/groupchats/{user_id}")
async def get_groupchats(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(GroupChat)
            .join(GroupChat.members)
            .options(selectinload(GroupChat.members))
            .filter(User.id == user_id)
        )
        group_chats = result.scalars().all()
        return group_chats
    except Exception as e:
        logging.error(f"Error fetching group chats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching group chats: {str(e)}"
        )


@router.get("/groupchats")
async def get_all_groupchats(db: AsyncSession = Depends(get_db)):
    """Fetch all groupchats from the database."""
    try:
        result = await db.execute(select(GroupChat))
        groupchats = result.scalars().all()
        return groupchats
    except Exception as e:
        logging.error(f"Error fetching groupchats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching groupchats: {str(e)}"
        )


@router.delete("/groupchats/{groupchat_id}")
async def delete_groupchat(
    groupchat_id: int, user_id: int, db: AsyncSession = Depends(get_db)
):
    groupchat = await db.get(GroupChat, groupchat_id)
    if not groupchat:
        raise HTTPException(status_code=404, detail="Group chat not found")
    if groupchat.admin_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this group chat"
        )

    await db.execute(
        delete(group_members).where(
            group_members.c.group_id == groupchat_id
        )
    )

    await db.delete(groupchat)
    await db.commit()
    return {"message": "Group chat deleted successfully"}
