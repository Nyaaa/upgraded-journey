import json
import os

import pytest
from mock import patch, mock_open

PASSAGE = {
    "beauty_title": "string",
    "title": "string",
    "other_titles": "string",
    "connect": "string",
    "level_winter": "string",
    "level_summer": "string",
    "level_autumn": "string",
    "level_spring": "string",
}
COORDS = {
    "latitude": 0,
    "longitude": 0,
    "height": 0
}
USER = {
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "middle_name": "string",
    "phone": "+7 111 11 11",
}
URL = '/v1/submitData/'


@pytest.mark.asyncio
async def test_pass_post_with_image(client):
    with patch("builtins.open", mock_open(read_data="data")):
        files = [('image_file', open("mock_file1", 'rb')), ('image_file', open("mock_file2", 'rb'))]
    response = await client.post(url=URL, files=files,
                                 data=dict(passage=json.dumps(PASSAGE),
                                           coords=json.dumps(COORDS),
                                           user=json.dumps(USER),
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
        os.remove(path)


@pytest.mark.asyncio
async def test_passes_get_one(client):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                         coords=json.dumps(COORDS),
                                         user=json.dumps(USER)))
    response = await client.get(f'{URL}1')
    assert response.status_code == 200
    assert response.json()['id'] == 1


@pytest.mark.asyncio
async def test_passes_get_one(client):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                         coords=json.dumps(COORDS),
                                         user=json.dumps(USER)))
    response = await client.get(f'{URL}?user__email=user%40example.com')
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_pass_patch(client):
    with patch("builtins.open", mock_open(read_data="data")):
        files = [('image_file', open("mock_file1", 'rb')), ('image_file', open("mock_file2", 'rb'))]
    await client.post(url=URL, files=files, data=dict(passage=json.dumps(PASSAGE),
                                                      coords=json.dumps(COORDS),
                                                      user=json.dumps(USER),
                                                      image_title='image_title1,image_title2',
                                                      )
                      )
    update = await client.patch(url=f'{URL}1', files=files,
                                data=dict(passage=json.dumps({"level_winter": "string"}),
                                          coords=json.dumps({"longitude": 0}),
                                          passage_id=1,
                                          image_title='image_title3,image_title4',
                                          )
                                )

    assert update.status_code == 200
    assert update.json() == {'state': 1, 'message': None}


@pytest.mark.asyncio
async def test_pass_patch_forbidden(client):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                         coords=json.dumps(COORDS),
                                         user=json.dumps(USER),
                                         )
                      )
    await client.patch(url=f'{URL}1', data=dict(passage=json.dumps({"status": "accepted"}), passage_id=1))
    update = await client.patch(url=f'{URL}1', data=dict(passage=json.dumps({"status": "pending"}), passage_id=1))

    assert update.status_code == 401
    assert update.json()['detail'] == {'state': 0, 'message': 'Only new submissions can be edited'}
