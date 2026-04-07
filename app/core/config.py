from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Pydantic automatically reads from .env file.
    """

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str = "db"
    DB_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        """Build the full PostgreSQL connection string."""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # App
    APP_NAME: str = "My API"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


# Single instance used across the whole app
settings = Settings()