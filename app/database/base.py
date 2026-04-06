from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, Integer
from datetime import datetime, timezone

class Base(DeclarativeBase):
    """
    Classe de base pour tous les models SQLAlchemy.
    Tous les models héritent de cette classe.
    """
    pass

class TimestampMixin:
    """
    Mixin réutilisable : ajoute created_at et updated_at
    à n'importe quel model.
    """
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
