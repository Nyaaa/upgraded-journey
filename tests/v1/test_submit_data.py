import json
import os

import pytest
from fastapi import HTTPException, UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import crud, models
from app.api.v1.routes import update_passage, read_passage_by_id, submit_data
from app.api.v1.schemas import (
    PassageUpdate,
    CoordsUpdate,
    UserBase,
    Coords,
    PassageBase,
)
from tests.sample_data import USER, USER2, PASSAGE, COORDS, FILES, BIN_FILE

URL = '/v1/submitData/'


@pytest.mark.asyncio
async def test_pass_post_with_image(client: AsyncClient):
    response = await client.post(
        url=URL,
        files=FILES,
        data=dict(
            passage=json.dumps(PASSAGE),
            coords=json.dumps(COORDS),
            user=json.dumps(USER2),
            image_title='image_title1,image_title2',
        ),
    )
    assert response.status_code == 200
    assert response.json()['id'] == 1

    passage = await client.get(url=f'{URL}1')
    passage = passage.json()['images']
    for path in passage:
        path = path['filepath']
        assert os.path.isfile(path)


@pytest.mark.asyncio
async def test_passes_get_one(
    create_passage: models.Passage, client: AsyncClient
):
    response = await client.get(f'{URL}1')
    assert response.status_code == 200
    assert response.json()['id'] == 1


@pytest.mark.asyncio
async def test_passes_404(async_session: AsyncSession):
    with pytest.raises(HTTPException) as err:
        await read_passage_by_id(1, async_session)
    assert err.value.status_code == 404
    assert err.value.detail == {'status': 404, 'message': 'Passage not found'}


@pytest.mark.asyncio
async def test_passes_get_by_email(
    create_passage: models.Passage, client: AsyncClient
):
    response = await client.get(f'{URL}?user__email=test%40example.com')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_pass_patch(client: AsyncClient):
    await client.post(
        url=URL,
        files=FILES,
        data=dict(
            passage=json.dumps(PASSAGE),
            coords=json.dumps(COORDS),
            user=json.dumps(USER2),
            image_title='image_title1,image_title2',
        ),
    )
    update = await client.patch(
        url=f'{URL}1',
        files=FILES,
        data=dict(
            passage=json.dumps({'level_winter': 'string'}),
            coords=json.dumps({'longitude': 0}),
            passage_id=1,
            image_title='image_title3,image_title4',
        ),
    )

    assert update.status_code == 200
    assert update.json() == {'state': 1, 'message': None}
    assert len(update.json()['images']) == 4


@pytest.mark.asyncio
async def test_pass_patch_status(
    create_passage: models.Passage, async_session: AsyncSession
):
    new_status = await update_passage(
        passage_id=1,
        passage=PassageUpdate(status='accepted'),
        db=async_session,
    )
    assert new_status.status_code == 200

    with pytest.raises(HTTPException) as err:
        await update_passage(
            passage_id=1,
            passage=PassageUpdate(status='pending'),
            db=async_session,
        )
    assert err.value.status_code == 401
    assert err.value.detail == {
        'state': 0,
        'message': 'Only new submissions can be edited',
    }


@pytest.mark.asyncio
async def test_pass_patch_image(
    create_passage: models.Passage, async_session: AsyncSession
):
    new_status = await update_passage(
        passage_id=1,
        image_title=['image_title1'],
        image_file=[UploadFile(file=BIN_FILE, filename='test')],
        coords=CoordsUpdate(),
        db=async_session,
    )
    assert new_status.status_code == 200


@pytest.mark.asyncio
async def test_pass_patch_invalid(
    async_session: AsyncSession, create_passage: models.Passage
):
    with pytest.raises(HTTPException) as err:
        await update_passage(passage_id=1, db=async_session)
    assert err.value.status_code == 400
    assert err.value.detail == {'state': 0, 'message': 'No data supplied'}


@pytest.mark.asyncio
async def test_submit_data_new_user(async_session: AsyncSession):
    user = await crud.get_all_objects(async_session, models.User)
    assert len(user) == 0
    await submit_data(
        passage=PassageBase(**PASSAGE),
        coords=Coords(**COORDS),
        user=UserBase(**USER2),
        image_title=['image_title1'],
        image_file=[UploadFile(file=BIN_FILE, filename='test')],
        db=async_session,
    )
    user = await crud.get_all_objects(async_session, models.User)
    assert len(user) == 1


async def test_submit_data_existing_user(
    async_session: AsyncSession, create_user: models.User
):
    user = await crud.get_all_objects(async_session, models.User)
    assert len(user) == 1
    await submit_data(
        passage=PassageBase(**PASSAGE),
        coords=Coords(**COORDS),
        user=UserBase(**USER),
        image_title=['image_title1'],
        image_file=[UploadFile(file=BIN_FILE, filename='test')],
        db=async_session,
    )
    user = await crud.get_all_objects(async_session, models.User)
    assert len(user) == 1


@pytest.mark.asyncio
async def test_pass_post_400(client: AsyncClient):
    response = await client.post(
        url=URL,
        data=dict(
            passage=json.dumps(PASSAGE),
            coords=json.dumps(COORDS),
        ),
    )
    assert response.status_code == 400
