from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Dict, Any
from app.core.config import settings

# Configuração do contexto de hash (usaremos bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import bcrypt

def get_password_hash(password: str) -> str:
    # Converte para bytes e trunca para 72 bytes (bcrypt limitação)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # bcrypt.compare_hash_and_password lida com o truncamento automático
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT com os dados fornecidos e tempo de expiração.
    Se expires_delta não for informado, usa o padrão do settings.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica um token JWT e retorna o payload se válido.
    Se inválido ou expirado, retorna None.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.JWTError:
        return None