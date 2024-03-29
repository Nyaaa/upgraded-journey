from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from .api.v1.routes import v1_app
from .api.v2.routes import v2_app
from .settings import settings

tags_metadata = [
    {
        'name': 'v1',
        'description': 'API version 1',
        'externalDocs': {'url': f'{settings.SERVER_HOST}/v1/docs'},
    },
    {
        'name': 'v2',
        'description': 'API version 2',
        'externalDocs': {'url': f'{settings.SERVER_HOST}/v2/docs'},
    },
]
app = FastAPI(root_path='', openapi_tags=tags_metadata)

app.mount('/v1', v1_app)
app.mount('/v2', v2_app)


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def get_api_versions() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title)
