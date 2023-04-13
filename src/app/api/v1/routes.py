from datetime import datetime
@app.post("/submitData/")
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

    return {'status': 200, 'message': None, 'id': passage.id}


from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422,
                        content=jsonable_encoder({"status": 422,
                                                  "message": exc.errors(),
                                                  "id": None}))


@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    return JSONResponse(status_code=500,
                        content=jsonable_encoder(
                            {"status": 500, "message": "Internal Server Error", "id": None}))
