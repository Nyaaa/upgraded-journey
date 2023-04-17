from datetime import datetime
from itertools import zip_longest
from typing import List

from fastapi import Depends, File, UploadFile, Body, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import crud, models
from app.db import get_db
from . import schemas

v1_app = FastAPI(version='1.1.0')


@v1_app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse(url="/v1/docs/")


@v1_app.post("/submitData/")
async def submit_data(image_title: List[str],
                      image_file: List[UploadFile] = File(...),
                      passage: schemas.PassageBase = Body(...),  # NOSONAR
                      coords: schemas.Coords = Body(...),
                      user: schemas.UserBase = Body(...),
                      db: AsyncSession = Depends(get_db)):
    get_user = await crud.get_user_by_email(db, email=user.email)
    if get_user:
        user = get_user
    else:
        user = models.User(**user.dict(), hashed_password='test')
        await crud.commit(db, user)
    coords = await crud.create_coords(db, coords)
    db_passage = models.Passage(**passage.dict(), add_time=datetime.utcnow(),
                                status='new', coords_id=coords.id, user_id=user.id)
    passage = await crud.commit(db, db_passage)

    if image_file:
        image_title = image_title[0].split(',') or None
        files = list(zip_longest(image_title, image_file, fillvalue=None))
        await crud.create_image(db, files, passage.id)

    return JSONResponse(status_code=200, content={'status': 200, 'message': None, 'id': passage.id})


@v1_app.get("/submitData/{passage_id}", response_model=schemas.Passage)
async def read_passage_by_id(passage_id: int, db: AsyncSession = Depends(get_db)):
    db_passage = await crud.get_object_by_id(db, model=models.Passage, obj_id=passage_id)
    if db_passage is None:
        raise HTTPException(status_code=404, detail={'status': 404, 'message': "Passage not found"})
    return db_passage


@v1_app.get("/submitData/", response_model=schemas.Passage)
async def read_passages(user__email: EmailStr = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_passage_by_email(db, email=user__email)


@v1_app.patch("/submitData/{passage_id}", response_model=schemas.Passage)
async def update_passage(passage_id: int,
                         passage: schemas.PassageUpdate,  # NOSONAR
                         db: AsyncSession = Depends(get_db)):
    db_passage = await read_passage_by_id(passage_id=passage_id, db=db)
    passage = dict(passage).items()
    for key, value in passage:
        setattr(db_passage, key, value) if value else None
    return await crud.commit(db, db_passage)


# @v1_app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return JSONResponse(status_code=400, content={"status": 400, "message": "Bad request", "id": None})
#
#
# @v1_app.exception_handler(500)
# async def internal_exception_handler(request, exc):
#     return JSONResponse(status_code=500, content={"status": 500, "message": "Internal Server Error", "id": None})
