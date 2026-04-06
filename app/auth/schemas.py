from pydantic import BaseModel, EmailStr

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

class RegisterDTO(BaseModel):
    email: EmailStr
    username: str
    password: str

class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenDTO(BaseModel):
    refresh_token: str
