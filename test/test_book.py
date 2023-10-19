import pytest

from app import models, schemas


def json_book():
    book = {
        "name":"updatename",
        "isbn":"1",
        "explanation":"updateexplanation"
    }
    return book



def test_get_all_books(test_books,authorized_client):
    res=authorized_client.get("/book")
    def validate(books):
        return schemas.BookOut(**books)
    books_map = map(validate,res.json())    
    books_list=list(books_map)
    assert len(books_list)==len(test_books)
    assert res.status_code == 200
    
def test_unauthorized_get_all_books(client,test_books):
    res = client.get("/book")
    assert res.status_code == 401

def test_get_one_book(client,test_books):
    res=client.get(f"/book/{test_books[0].isbn}")
    book=schemas.BookOut(**res.json())
    assert book.Book.isbn == test_books[0].isbn
    assert book.Book.name == test_books[0].name
    assert book.Book.explanation == test_books[0].explanation
    
    assert res.status_code == 200
    
def test_get_one_book_not_exist(client, test_books):
    res = client.get(f"/posts/88888")
    assert res.status_code == 404

def test_create_book(authorized_client,test_user):
    book=json_book()
    res = authorized_client.post("/book",json=book)
    created_book = schemas.Book(**res.json())
    assert res.status_code == 201
    assert created_book.name == book["name"]
    assert created_book.isbn == book["isbn"]
    assert created_book.explanation == book["explanation"]
    assert created_book.owner.id == test_user["id"]
    
    
def test_unauthorized_create_book(client):
    book = json_book()
    res = client.post("/book",json=book)
    assert res.status_code == 401 

def test_unauthorized_delete_book(client,test_books):
    res = client.delete(f"/book/{test_books[0].id}")
    assert res.status_code == 401
    
    
def test_delete_other_user_book(authorized_client,test_books2):
    res = authorized_client.delete(f"/book/{test_books2[0].id}")
    assert res.status_code == 403

def test_delete_book(authorized_client,test_books,sesssion):
    deleted_id=test_books[0].id
    res = authorized_client.delete(f"/book/{deleted_id}") 
    assert res.status_code == 204
    deleted_book = sesssion.query(models.Book).filter(models.Book.id == deleted_id).first()
    assert deleted_book == None
   
def test_delete_no_exist_book(authorized_client,test_books):
    res = authorized_client.delete("/book/80000")
    assert res.status_code == 404
    
def test_update_book(authorized_client,test_books):
    book = json_book()
    res = authorized_client.put(f"/book/{test_books[0].id}",json = book)
    
    updated_book=schemas.Book(**res.json())
    
    assert res.status_code == 200 
    assert updated_book.name == book["name"]
    assert updated_book.isbn == book["isbn"]
    assert updated_book.explanation == book["explanation"]
    
def test_update_other_user_book(authorized_client,test_books2):
    book = json_book()
    update_id = test_books2[0].id
    res = authorized_client.put(f"/book/{update_id}", json = book)
    assert res.status_code == 403
    
def test_update_no_exist_book(authorized_client):
    book = json_book()
    res = authorized_client.put("/book/80000",json = book)
    assert res.status_code == 404
    
def test_unauthorized_update_book(client,test_books):
    book = json_book()
    update_id = test_books[0].id
    res = client.put(f"/book/{update_id}")
    assert res.status_code == 401