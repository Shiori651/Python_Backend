from pydantic import BaseModel,EmailStr,conint
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    
class UserLogin(UserBase):
    password:str
    
class UserCreat(UserLogin):
    name:str
    


class UserOut(UserBase):
    id:int
    name:str
    created_at:datetime
    class Config:
        from_attributes=True
        

class BookBase(BaseModel):
    name:str
    isbn:str
    explanation:str
    
class BookCreate(BookBase):
    pass
    
class Book(BookBase):
    id:int
    owner:UserOut
    class Config:
        from_attributes =True


class BookOut(BaseModel):
    Book:Book
    laybarys:int
    class Config:
        from_attributes =True
class library(BaseModel):
    book_id:int




class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[int]