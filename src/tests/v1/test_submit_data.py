import json
import os
from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile

from tests.sample_data import USER2, PASSAGE, COORDS, FILES
from app.api.v1.routes import update_passage
from app.api.v1.schemas import PassageUpdate, CoordsUpdate

URL = '/v1/submitData/'


@pytest.mark.asyncio
async def test_pass_post_with_image(client, cleanup):
    response = await client.post(url=URL, files=FILES,
                                 data=dict(passage=json.dumps(PASSAGE),
                                           coords=json.dumps(COORDS),
                                           user=json.dumps(USER2),
                                           image_title='image_title1,image_title2',
                                           )
                                 )
    assert response.status_code == 200
    assert response.json()['id'] == 1

    passage = await client.get(url=f'{URL}1')
    passage = passage.json()['images']
    for path in passage:
        path = path['filepath']
        assert os.path.isfile(path)


@pytest.mark.asyncio
async def test_passes_get_one(client):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                         coords=json.dumps(COORDS),
                                         user=json.dumps(USER2)))
    response = await client.get(f'{URL}1')
    assert response.status_code == 200
    assert response.json()['id'] == 1


@pytest.mark.asyncio
async def test_passes_get_by_email(client):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                         coords=json.dumps(COORDS),
                                         user=json.dumps(USER2)))
    response = await client.get(f'{URL}?user__email=user2%40example.com')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_pass_patch(client, cleanup):
    await client.post(url=URL, files=FILES, data=dict(passage=json.dumps(PASSAGE),
                                                      coords=json.dumps(COORDS),
                                                      user=json.dumps(USER2),
                                                      image_title='image_title1,image_title2',
                                                      )
                      )
    update = await client.patch(url=f'{URL}1', files=FILES,
                                data=dict(passage=json.dumps({"level_winter": "string"}),
                                          coords=json.dumps({"longitude": 0}),
                                          passage_id=1,
                                          image_title='image_title3,image_title4',
                                          )
                                )

    assert update.status_code == 200
    assert update.json() == {'state': 1, 'message': None}


@pytest.mark.asyncio
async def test_pass_patch_status(client, async_session):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                         coords=json.dumps(COORDS),
                                         user=json.dumps(USER2),
                                         )
                      )
    _bin = BytesIO('test'.encode('utf-8'))
    new_status = await update_passage(passage_id=1,
                                      passage=PassageUpdate(status='accepted'),
                                      image_file=None,
                                      db=async_session)
    assert new_status.status_code == 200

    with pytest.raises(HTTPException) as err:
        await update_passage(passage_id=1, passage=PassageUpdate(status='pending'), db=async_session)
    assert err.value.status_code == 401
    assert err.value.detail == {'state': 0, 'message': 'Only new submissions can be edited'}


@pytest.mark.asyncio
async def test_pass_patch(client, async_session, cleanup):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                         coords=json.dumps(COORDS),
                                         user=json.dumps(USER2),
                                         )
                      )
    _bin = BytesIO('test'.encode('utf-8'))
    new_status = await update_passage(passage_id=1,
                                      image_title=['image_title1'],
                                      image_file=[UploadFile(file=_bin, filename='test')],
                                      coords=CoordsUpdate(),
                                      db=async_session)
    assert new_status.status_code == 200
