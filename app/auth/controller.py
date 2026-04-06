from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.schemas import LoginDTO, RegisterDTO, TokenResponseDTO, RefreshTokenDTO
from app.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponseDTO, status_code=201)
async def register(data: RegisterDTO, db: AsyncSession = Depends(get_db)):
    """Inscription d'un nouvel utilisateur"""
    return await AuthService(db).register(data)

@router.post("/login", response_model=TokenResponseDTO)
async def login(data: LoginDTO, db: AsyncSession = Depends(get_db)):
    """Connexion et obtention des tokens JWT"""
    return await AuthService(db).login(data)

@router.post("/refresh", response_model=TokenResponseDTO)
async def refresh(data: RefreshTokenDTO, db: AsyncSession = Depends(get_db)):
    """Renouveler l'access token avec le refresh token"""
    return await AuthService(db).refresh(data.refresh_token)
