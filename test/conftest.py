from app import models
from . import test_database
import pytest
from app.oauth2 import creat_access_token 

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
def test_books(test_user, sesssion, test_user2):
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
        },{
            "name":"name4",
            "isbn":"4",
            "explanation":"explanation4",
            "owner_id":test_user2["id"]    
        },
    ]
    def create_books(book):
        return models.Book(**book)
    books_map=map(create_books,books_data)
    book=list(books_map)
    sesssion.add_all(book)
    sesssion.commit()
    books=sesssion.query(models.Book).all()
    return books
    
    