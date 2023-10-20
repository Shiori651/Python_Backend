from app import schemas,models
import pytest


@pytest.fixture()
def test_library(sesssion,test_user,test_books2):
    book_id=test_books2[0].id
    new_library = models.Library(user_id=test_user["id"], book_id = book_id)
    sesssion.add(new_library)
    sesssion.commit()
    return book_id

def library_json(book_id,dir):
    json = {
        "book_id":book_id,
        "dir":dir
    }
    return json

def test_add_libray(authorized_client,test_books2):
    json = library_json(test_books2[0].id, dir=1)
    
    res=authorized_client.post("/library",json=json)
    assert res.status_code == 201
    
def test_delete_library(authorized_client, test_library):
    json = library_json(test_library, dir=0)
    
    res = authorized_client.post("/library",json=json)
    assert res.status_code == 200
    
def test_twice_add_library(authorized_client, test_library):
    json = library_json(test_library,dir=1)
    
    res = authorized_client.post("/library", json=json)
    assert res.status_code == 409
    
def test_delete_libary_no_exist(authorized_client,test_books2):
    json = library_json(test_books2[0].id, dir=0)
    
    res = authorized_client.post("/library", json=json)
    assert res.status_code == 404

def test_library_no_exist_book(authorized_client,test_books2):
    json = library_json(book_id=8000 ,dir = 1)
    
    res = authorized_client.post("/library", json=json)
    assert res.status_code == 404
    
def test_unauthorized_library(client,test_books2):
    json = library_json(book_id=test_books2[0].id, dir=1)
    
    res = client.post("/library", json=json)
    assert res.status_code == 401