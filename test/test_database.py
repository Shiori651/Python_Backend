from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base,get_db
from app.config import settings
from app.main import app
import pytest

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engin=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal= sessionmaker(autocommit=False,autoflush= False,bind=engin)

@pytest.fixture()
def sesssion():
    Base.metadata.drop_all(bind=engin)
    Base.metadata.create_all(bind=engin)
    dp=TestingSessionLocal()
    try:
        yield dp
    finally:
        dp.close()

@pytest.fixture()
def client(sesssion):
    def override_get_db():
        dp=TestingSessionLocal()
        try:
            yield sesssion
        finally:
            sesssion.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


