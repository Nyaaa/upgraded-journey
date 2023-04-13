from datetime import datetime
from itertools import zip_longest
from typing import List

from fastapi import Depends, File, UploadFile, Body, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi_versionizer.versionizer import api_version, api_version_remove
from sqlalchemy.orm import Session

from app.api import crud, models, schemas
from app.db import get_db

router = APIRouter()


@router.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/v1/docs/")


@api_version(1)
@api_version_remove(2)
@router.post("/submitData")
async def submit_data(image_title: List[str],
                      image_file: List[UploadFile] = File(...),
                      passage: schemas.PassageBase = Body(...),  # NOSONAR
                      coords: schemas.Coords = Body(...),
                      user: schemas.UserBase = Body(...),
                      db: Session = Depends(get_db)):
    get_user = crud.get_user_by_email(db, email=user.email)
    if get_user:
        user = get_user
    else:
        user = models.User(**user.dict())
        crud.commit(db, user)
    coords = crud.create_coords(db, coords)
    db_passage = models.Passage(**passage.dict(), add_time=datetime.utcnow(),
                                status='new', coords_id=coords.id, user_id=user)
    passage = crud.commit(db, db_passage)

    if image_file:
        image_title = image_title[0].split(',') or None
        files = list(zip_longest(image_title, image_file, fillvalue=None))
        await crud.create_image(db, files, passage.id)

    return JSONResponse(status_code=200, content={'status': 200, 'message': None, 'id': passage.id})
