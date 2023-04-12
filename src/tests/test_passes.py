import json
import os

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


def test_pass_get_all(client):
    response = client.get("/passages/")
    assert response.status_code == 200


def test_pass_post_no_image(client, create_user):
    response = client.post(url="/submitData/", data=dict(passage=json.dumps(PASSAGE),
                                                         coords=json.dumps(COORDS)))
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_pass_post_with_image(client, create_user):
    response = client.post(url="/submitData/",
                           data=dict(passage=json.dumps(PASSAGE),
                                     coords=json.dumps(COORDS),
                                     image_title='image_title1',
                                     ),
                           files={'image_file': open("./tests/281.jpg", 'rb')}
                           )
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()["images"]) == 1
