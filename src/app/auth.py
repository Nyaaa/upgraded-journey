from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app import db, hasher
from app.api import crud, models

security = HTTPBasic()


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    _db: AsyncSession = Depends(db.get_db),
) -> models.User:
    user_login = credentials.username
    user_password = credentials.password
    verified = False
    user = await crud.get_user_by_email(db=_db, email=user_login)
    if user:
        verified = hasher.verify(user_password, user.hashed_password)

    if not (user and verified):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
