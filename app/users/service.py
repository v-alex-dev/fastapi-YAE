from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.users.model import User
from app.users.schemas import UserResponseDTO, UserToken

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profil(self, current_user: UserToken) -> UserResponseDTO:
        """Fetch authenticated user profile from DB using JWT payload"""
        result = await self.db.execute(
            select(User).where(User.id == int(current_user.sub))
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponseDTO.model_validate(user)