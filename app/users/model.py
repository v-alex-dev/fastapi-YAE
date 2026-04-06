from sqlalchemy import Column, String, Boolean, Enum as SAEnum
from app.database.base import Base, TimestampMixin
from app.enums.roles import RoleEnum

class User(Base, TimestampMixin):
    """
    Model SQLAlchemy = représentation de la table en BDD.
    NE JAMAIS exposer directement ce model dans les réponses API.
    Toujours passer par un DTO/Schema Pydantic.
    """
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SAEnum(RoleEnum), default=RoleEnum.USER, nullable=False)
