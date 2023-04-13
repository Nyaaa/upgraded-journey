from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi_versionizer.versionizer import versionize

from .api import models
from .api.v1.routes import router as router_v1
from .api.v2.routes import router as router_v2
from .db import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
router = APIRouter()

app.include_router(router_v1)
app.include_router(router_v2)

versions = versionize(
    app=app,
    prefix_format='/v{major}',
    docs_url='/docs',
    redoc_url='/redoc'
)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def get_api_versions() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title)
