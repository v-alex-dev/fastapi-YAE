from app.core.config import settings
from app.database.base import Base
from app.users.model import User  # import obligatoire pour que le model soit détecté

config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata