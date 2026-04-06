from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.enums.roles import RoleEnum

# ─── Input DTOs ───────────────────────────────────────────────

class CreateUserDTO(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class UpdateUserDTO(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    is_active: bool | None = None

# ─── Output DTOs ─────────────────────────────────────────────

class UserResponseDTO(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

# ─── Token payload (decoded JWT data) ────────────────────────

class UserToken(BaseModel):
    """Represents the decoded JWT payload — injected via Depends"""
    sub: str        # user id as string
    role: str       # role value