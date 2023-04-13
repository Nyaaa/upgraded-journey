from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.models import User
from app.db import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    yield app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(test_app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(test_app: FastAPI, db_session: SessionTesting
           ) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    test_app.dependency_overrides[get_db] = _get_test_db
    with TestClient(test_app) as client:
        yield client


@pytest.fixture()
def create_user(db_session):
    user = User(email='test@example.com',
                first_name='first_name',
                last_name='last_name')
    db_session.add(user)
    db_session.commit()
