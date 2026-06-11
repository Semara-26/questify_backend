from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str


# --- User Schemas ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, description="Nama tampilan user")
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    level: int
    exp: int
    coins: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --- Quest Schemas ---
class QuestCreate(BaseModel):
    title: str = Field(..., description="Judul atau deskripsi quest")
    rank: Literal["S", "A", "B", "C", "D"] = Field(
        ..., description="Rank quest: D, C, B, A, atau S"
    )


class QuestResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    rank: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# --- Reward Schemas ---
class RewardCreate(BaseModel):
    title: str = Field(..., description="Nama hadiah atau reward")
    cost: int = Field(
        ..., gt=0, description="Harga koin untuk redeem (harus lebih dari 0)"
    )


class RewardResponse(BaseModel):
    id: UUID
    title: str
    cost: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
