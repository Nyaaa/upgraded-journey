from datetime import timedelta
from itertools import zip_longest
from typing import List, Optional

from fastapi import Depends, File, UploadFile, Body, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import auth
from app.api import crud, schemas, models
from app.db import get_db

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users.",
    },
    {
        "name": "Passes",
        "description": "Operations with mountain passes.",
    },
]
v2_app = FastAPI(version="2.1.0", openapi_tags=tags_metadata)


@v2_app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse(url="/v2/docs/")


@v2_app.post("/users/", response_model=schemas.User, tags=["Users"])
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Email already registered",
            },
        )
    user_dict = user.dict()
    hashed_password = auth.str_to_hash(user_dict.pop("password"))
    user = models.User(**user_dict | {"hashed_password": hashed_password})
    return await crud.commit(db=db, instance=user)


@v2_app.get(
    "/users/",
    response_model=list[schemas.User],
    tags=["Users"],
    response_model_exclude={"passages"},
)
async def read_all_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_objects(db, model=models.User, skip=skip, limit=limit)


@v2_app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_object_by_id(db, model=models.User, obj_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": status.HTTP_404_NOT_FOUND, "message": "User not found"},
        )
    return db_user


@v2_app.post("/token", response_model=schemas.Token, tags=["Users"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@v2_app.get("/users/me/", response_model=schemas.User, tags=["Users"])
async def read_users_me(
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return current_user


@v2_app.post("/passages/", response_model=schemas.Passage, tags=["Passes"])
async def create_passage(
    user: models.User = Depends(auth.get_current_active_user),
    image_title: Optional[List[str]] = None,
    image_file: Optional[List[UploadFile]] = File(None),
    passage: schemas.PassageBase = Body(...),  # NOSONAR
    coords: schemas.Coords = Body(...),
    db: AsyncSession = Depends(get_db),
):
    coords = await crud.create_coords(db, coords)
    passage = await crud.create_passage(
        db=db, passage=passage, coords=coords, user=user
    )

    if image_file and isinstance(image_file, list):
        image_title = image_title[0].split(",") or None
        files = list(zip_longest(image_title, image_file, fillvalue=None))
        await crud.create_image(db, files, passage.id)

    await db.refresh(passage)
    return passage


@v2_app.get("/passages/", response_model=list[schemas.Passage], tags=["Passes"])
async def read_all_passages(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_objects(db, model=models.Passage, skip=skip, limit=limit)


@v2_app.get("/passages/{passage_id}", response_model=schemas.Passage, tags=["Passes"])
async def read_passage_by_id(passage_id: int, db: AsyncSession = Depends(get_db)):
    db_passage = await crud.get_object_by_id(
        db, model=models.Passage, obj_id=passage_id
    )
    if db_passage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Passage not found",
            },
        )
    return db_passage
