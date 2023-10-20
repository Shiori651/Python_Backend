from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from app.oauth2 import creat_access_token 
from app.database import Base,get_db
from app.config import settings
from app.main import app
from app import models
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engin=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal= sessionmaker(autocommit=False,autoflush= False,bind=engin)

@pytest.fixture()
def sesssion():

    Base.metadata.drop_all(bind=engin)
    Base.metadata.create_all(bind=engin)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(sesssion):
    def override_get_db():
        db=TestingSessionLocal()
        try:
            yield sesssion
        finally:
            sesssion.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"email":"test123@gmail.com",
               "password":"test123",
               "name":"test"
               }
    res = client.post("/user",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {"email":"test321@gmail.com",
               "password":"test321",
               "name":"test"
               }
    res = client.post("/user",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def token(test_user):
    token = creat_access_token({"user_id":test_user["id"]})
    return token
    
@pytest.fixture()
def authorized_client(token,client):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_books(test_user, sesssion):
    books_data=[
        {
            "name":"name1",
            "isbn":"1",
            "explanation":"explanation1",
            "owner_id":test_user["id"]
        },{
            "name":"name2",
            "isbn":"2",
            "explanation":"explanation2",
            "owner_id":test_user["id"]  
             
        },{
            "name":"name3",
            "isbn":"3",
            "explanation":"explanation3",
            "owner_id":test_user["id"]  
        }
    ]
    def create_books(book):
        return models.Book(**book)
    books_map=map(create_books,books_data)
    book=list(books_map)
    sesssion.add_all(book)
    sesssion.commit()
    books=sesssion.query(models.Book).all()
    return books
    
    

@pytest.fixture()
def test_books2(sesssion, test_user2):
    books_data=[
        {
            "name":"name1",
            "isbn":"1",
            "explanation":"explanation1",
            "owner_id":test_user2["id"]
        },{
            "name":"name2",
            "isbn":"2",
            "explanation":"explanation2",
            "owner_id":test_user2["id"]  
             
        },{
            "name":"name3",
            "isbn":"3",
            "explanation":"explanation3",
            "owner_id":test_user2["id"]  
        }
    ]
    def create_books(book):
        return models.Book(**book)
    books_map=map(create_books,books_data)
    book=list(books_map)
    sesssion.add_all(book)
    sesssion.commit()
    books=sesssion.query(models.Book).all()
    return books
    