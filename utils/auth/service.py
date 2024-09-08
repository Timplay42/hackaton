from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy import select
from api.Users.model import Users

from utils.base.config import settings
from utils.base.database_session import AsyncDatabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login", scheme_name="JWT")

async def validate_auth_user(username: str = Form(), password: str = Form()):
        session = await AsyncDatabase.return_session()

        user = (await session.scalars(select(Users).where(Users.username == username))).first() 
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid username or password")

        if not validate_password(
            password=password,
            hashed_password=user.password,
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid username or password')

        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user inactive",
            )

        return user


async def encode_jwt(
    payload: dict,
    private_key: str = settings.key.private_key_path.read_text(),
    algorithm: str = settings.key.algoritm,
) -> str:
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded


async def decode_jwt(
    token: str | bytes,
    public_key: str = settings.key.public_key_path.read_text(),
    algorithm: str = settings.key.algoritm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


async def hash_password(password: str,) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )

async def get_me(token: str = Depends(oauth2_scheme)):
        if not token:
            raise HTTPException(status_code=401, detail="Token not provided")
        try:
            payload = decode_jwt(token=token)

        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}")
        
        session = await AsyncDatabase.return_session()
        try:
            query = await session.scalars(select(Users).where(Users.id == payload.get('user_id')))
            user = query.first()
            if user.active is False:
                raise HTTPException(status_code=401, detail="User deactivate")
            return user
        finally:
            await session.close()
