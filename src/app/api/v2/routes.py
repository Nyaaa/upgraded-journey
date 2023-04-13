from itertools import zip_longest
from typing import List, Optional

from fastapi import Depends, File, UploadFile, Body, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi_versionizer.versionizer import api_version
from sqlalchemy.orm import Session

from app.api import crud, schemas
from app.db import get_db

router = APIRouter()


@api_version(2)
@router.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/v2/docs/")


@api_version(2)
@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return JSONResponse(status_code=400, content={'status': 400, 'message': "Email already registered"})
    return crud.create_user(db=db, user=user)


@api_version(2)
@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@api_version(2)
@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        return JSONResponse(status_code=404, content={'status': 404, 'message': "User not found"})
    return db_user


@api_version(2)
@router.post("/passages/", response_model=schemas.Passage)
async def create_passage(image_title: Optional[List[str]] = None,
                         image_file: Optional[List[UploadFile]] = File(None),
                         passage: schemas.PassageCreate = Body(...),  # NOSONAR
                         coords: schemas.Coords = Body(...),
                         db: Session = Depends(get_db)):
    passage.user_id = read_user(user_id=passage.user_id, db=db).id
    coords = crud.create_coords(db, coords)
    passage = crud.create_passage(db=db, passage=passage, coords=coords)

    if image_file:
        image_title = image_title[0].split(',') or None
        files = list(zip_longest(image_title, image_file, fillvalue=None))
        await crud.create_image(db, files, passage.id)

    return passage


@api_version(2)
@router.get("/passages/", response_model=list[schemas.Passage])
async def read_passages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_passages(db, skip=skip, limit=limit)
