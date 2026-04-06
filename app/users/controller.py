from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.core.dependencies import get_current_active_user
from app.users.schemas import UpdateUserDTO, CreateUserDTO, UserResponseDTO, UserToken
from app.users.service import UserService

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/profil", response_model=UserResponseDTO)
async def profil(
    current_user: UserToken = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the authenticated user's profile"""
    return await UserService(db).get_profil(current_user)