import pytest
from app import schemas
from app.config import settings
from jose import jwt
from .test_database import client,sesssion
from .conftest import test_user

def current_user_schema(
        email="test123@gmail.com",
        password="test123456"
        ):
    user_login={"username":email,"password":password}
    return user_login

def test_create_user(client):
    res=client.post("/user",json={"email":"test123@gmail.com","password":"test123456","name":"test"})
    new_user=schemas.UserOut(**res.json())
    assert new_user.email=="test123@gmail.com"
    assert res.status_code==201

def test_login_user(client,test_user):
    res = client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(token=login_res.access_token,algorithms=settings.algorithm,key=settings.secret_key)
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize(
    "email, password, status_code",[
        ("worngemail@gmail.com","test123456",404),
        ("test123@gmail.com","wrongpassword",404),
        ("wrongemail@gmail.com","wrongpassword",404),
        (None,"test123456",422),
        ("test123@gmail.com",None,422)
    ])
def test_incurrent_login(client,email,password,status_code):
    res = client.post("/login",data={"username":email,"password":password})
    assert res.status_code == status_code