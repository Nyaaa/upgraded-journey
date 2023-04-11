from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from .api import crud, models, schemas
from .db import SessionLocal, engine
import aiofiles
from typing import List

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
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
def create_passage(passage: schemas.PassageCreate, db: Session = Depends(get_db)):
    passage.user_id = read_user(user_id=passage.user_id, db=db).id
    passage.coords = crud.create_coords(db, passage.coords)
    return crud.create_passage(db=db, passage=passage)


@app.get("/passages/", response_model=list[schemas.Passage])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_passages(db, skip=skip, limit=limit)


@app.post("/upload-file", response_model=list[schemas.Image])
async def create_upload_file(title: List[str],
                             passage_id: int,
                             file: List[UploadFile] = File(...),
                             db: Session = Depends(get_db)):

    title = title[0].split(',')
    files = list(zip(title, file))
    to_save = []

    for title, file in files:
        file_path = "./media/" + file.filename

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)

        to_save.append(models.Image(title=title, passage_id=passage_id, filepath=file_path))
    crud.create_image(db, to_save)
    return to_save
