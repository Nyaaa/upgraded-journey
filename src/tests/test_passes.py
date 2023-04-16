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
    "user_id": 1
}
COORDS = {
    "latitude": 0,
    "longitude": 0,
    "height": 0
}
URL = '/v2/passages/'


@pytest.mark.asyncio
async def test_pass_get_all(client):
    response = await client.get(URL)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_pass_post_no_image(client, create_user):
    response = await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE),
                                              coords=json.dumps(COORDS)))
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["status"] == "new"


@pytest.mark.asyncio
async def test_pass_post_with_image(client, create_user):
    with patch("builtins.open", mock_open(read_data="data")):
        files = [('image_file', open("mock_file1", 'rb')), ('image_file', open("mock_file2", 'rb'))]
    response = await client.post(url=URL,
                           data=dict(passage=json.dumps(PASSAGE),
                                     coords=json.dumps(COORDS),
                                     image_title='image_title1,image_title2',
                                     ),
                           files=files
                           )
    assert response.status_code == 200
    assert len(response.json()["images"]) == 2

    for path in response.json()["images"]:
        path = path['filepath']
        assert os.path.isfile(path)
        os.remove(path)
