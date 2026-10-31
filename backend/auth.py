from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt

# Configurações de Segurança - EM PRODUÇÃO, ISSO DEVE ESTAR EM VARIÁVEIS DE AMBIENTE (.env)
SECRET_KEY = "UMA_CHAVE_MUITO_SECRETA_E_LONGA_123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def verify_password(plain_password: str, hashed_password: str):
    # O bcrypt espera bytes, então codificamos as strings para utf-8
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_password_hash(password: str):
    # Gera o sal e o hash em uma única operação
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Retornamos como string para salvar no banco de dados
    return hashed_password.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
