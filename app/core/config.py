from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Pydantic lit automatiquement le fichier .env
    et valide les types. Si une var est manquante → erreur claire.
    """
    app_name: str = "API-YAE"
    debug: bool = False
    secret_key: str

    # JWT
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # BDD
    db_user: str
    db_password: str
    db_name: str
    db_host: str = "db"
    db_port: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = ".env"

# lru_cache → créé une seule fois, réutilisé partout (Singleton)
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
