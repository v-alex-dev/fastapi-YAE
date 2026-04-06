from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Contexte bcrypt pour hasher les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Transforme 'mypassword' en '$2b$12$...' (irréversible)"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare le mot de passe saisi avec le hash stocké"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Crée un JWT signé avec la SECRET_KEY.
    Le payload contient : sub (user_id), exp (expiration), type.
    Quiconque peut LIRE le payload (base64), mais ne peut pas
    le MODIFIER sans invalider la signature → sécurité garantie.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload.update({"exp": expire, "type": "access"})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(data: dict) -> str:
    """Token longue durée pour renouveler l'access token"""
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    payload.update({"exp": expire, "type": "refresh"})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> dict:
    """Décode et vérifie la signature + expiration du token"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None
