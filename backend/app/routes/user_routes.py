from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.database import get_db
from pydantic import BaseModel

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: str


class UserSignIn(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered",
        )

    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/signin", response_model=UserResponse)
async def signin(signin: UserSignIn, db: AsyncSession = Depends(get_db)):
    print(20 * "*")
    print("signin")
    result = await db.execute(select(User).where(User.username == signin.username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found",
        )
    return user


@router.get("/users/{username}")
async def get_user_byname(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
