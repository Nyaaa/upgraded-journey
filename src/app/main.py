from itertools import zip_longest
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Body
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from .api import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(root_path='/api')
api_v1 = FastAPI()
api_v2 = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get("/")
# def main():
#     return RedirectResponse(url="/docs/")


@api_v1.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@api_v1.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/passages/", response_model=schemas.Passage)
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


@app.get("/passages/", response_model=list[schemas.Passage])
def read_passages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_passages(db, skip=skip, limit=limit)


app.mount('/v1', api_v1)
app.mount('/v2', api_v2)
