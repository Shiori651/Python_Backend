from app import schemas
from .conftest import authorized_client, test_user, test_user2,test_books
from .test_database import client, sesssion

def test_get_all_books(test_books,authorized_client):
    res=authorized_client.get("/book")
    def validate(books):
        return schemas.BookOut(books)
    # I will continue from here
    
