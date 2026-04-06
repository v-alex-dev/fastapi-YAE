from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

# Moteur async (performances meilleures avec FastAPI)
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,   # Log les requêtes SQL en mode debug
    pool_size=10,           # Connexions simultanées max
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """
    Dependency Injection FastAPI.
    Utilisé dans les controllers via : db: AsyncSession = Depends(get_db)
    Garantit que la session est fermée après chaque requête.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
