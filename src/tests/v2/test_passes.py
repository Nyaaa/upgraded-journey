import json
import os

import pytest
from tests.sample_data import COORDS, PASSAGE_WITH_USER, FILES


URL = '/v2/passages/'


@pytest.mark.asyncio
async def test_pass_get_all(client):
    response = await client.get(URL)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_pass_post_no_image(client, create_user):
    response = await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE_WITH_USER),
                                                    coords=json.dumps(COORDS)))
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["status"] == "new"


@pytest.mark.asyncio
async def test_pass_post_with_image(client, create_user, cleanup):
    response = await client.post(url=URL, files=FILES,
                                 data=dict(passage=json.dumps(PASSAGE_WITH_USER),
                                           coords=json.dumps(COORDS),
                                           image_title='image_title1,image_title2',
                                           )
                                 )
    assert response.status_code == 200
    assert len(response.json()["images"]) == 2

    for path in response.json()["images"]:
        path = path['filepath']
        assert os.path.isfile(path)


@pytest.mark.asyncio
async def test_passes_get_one(client, create_user):
    await client.post(url=URL, data=dict(passage=json.dumps(PASSAGE_WITH_USER),
                                         coords=json.dumps(COORDS)))
    response = await client.get(f'{URL}1')
    assert response.status_code == 200
    assert response.json()['id'] == 1
