import os
from io import BytesIO

import pytest
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import crud
from app.api import models
from tests.sample_data import USER2, USER


@pytest.mark.asyncio
async def test_get_obj_by_id(
    async_session: AsyncSession, create_user: models.User
):
    result = await crud.get_object_by_id(async_session, models.User, 1)
    assert result.id == 1


@pytest.mark.asyncio
async def test_get_all_obj(
    async_session: AsyncSession, create_user: models.User
):
    user = models.User(**USER2)
    async_session.add(user)
    await async_session.commit()
    result = await crud.get_all_objects(async_session, models.User)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_user_by_email(
    async_session: AsyncSession, create_user: models.User
):
    result = await crud.get_user_by_email(async_session, USER['email'])
    assert result.email == USER['email']


@pytest.mark.asyncio
async def test_commit(async_session: AsyncSession):
    user = models.User(**USER2)
    result = await crud.commit(async_session, user)
    assert isinstance(result, models.User)


@pytest.mark.asyncio
async def test_get_passage_by_email(
    async_session: AsyncSession, create_passage: models.Passage
):
    result = await crud.get_passage_by_email(async_session, USER['email'])
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], models.Passage)
    assert result[0].user_id == 1


@pytest.mark.asyncio
async def test_write_file_to_hdd(async_session: AsyncSession):
    orig_db_url = async_session.bind.url
    async_session.bind.url = 'test'
    _bin = BytesIO('test'.encode('utf-8'))
    files = [('image_title1', UploadFile(file=_bin, filename='test'))]
    saved = await crud.create_image(async_session, files, 1)
    async_session.bind.url = orig_db_url

    path = saved[0].filepath
    assert os.path.isfile(path)
    assert isinstance(saved, list)
    assert isinstance(saved[0], models.Image)
    os.remove(path)
    parent = os.path.dirname(path)
    if len(os.listdir(parent)) == 0:
        os.rmdir(parent)
