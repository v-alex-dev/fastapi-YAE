from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.users.model import User
from app.auth.schemas import LoginDTO, RegisterDTO, TokenResponseDTO
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: RegisterDTO) -> TokenResponseDTO:
        # Vérifie si l'email existe déjà
        result = await self.db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password)
        )
        self.db.add(user)
        await self.db.flush()  # Obtenir l'id sans commit

        return self._generate_tokens(user)

    async def login(self, data: LoginDTO) -> TokenResponseDTO:
        result = await self.db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()

        # Message générique volontairement : ne pas indiquer si c'est
        # l'email ou le password qui est faux (sécurité)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account disabled"
            )

        return self._generate_tokens(user)

    async def refresh(self, refresh_token: str) -> TokenResponseDTO:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        result = await self.db.execute(
            select(User).where(User.id == int(payload["sub"]))
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return self._generate_tokens(user)

    def _generate_tokens(self, user: User) -> TokenResponseDTO:
        token_data = {"sub": str(user.id), "role": user.role.value}
        return TokenResponseDTO(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data)
        )
