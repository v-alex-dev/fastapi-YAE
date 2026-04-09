from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Fields shared between create and read schemas."""
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Schema for POST /users — includes password."""
    password: str


class UserUpdate(BaseModel):
    """Schema for PATCH /users/{id} — all fields optional."""
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema returned by the API — never exposes the password."""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = {"from_attributes": True}  # Allows reading from ORM objects