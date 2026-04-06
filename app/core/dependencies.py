from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.users.model import User
from app.users.schemas import UserToken
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserToken:
    """Decodes the Bearer token and returns the payload as UserToken"""
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserToken(sub=payload["sub"], role=payload["role"])

async def get_current_active_user(
    current_user: UserToken = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ) -> UserToken:
    """Checks that the user account is still active in DB"""
    result = await db.execute(select(User).where(User.id == int(current_user.sub)))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disabled",
        )

    return current_user