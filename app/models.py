from sqlalchemy import Column, Integer,String,Boolean,DateTime,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base


class Book(Base):
    __tablename__="books"
    
    id= Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    isbn=Column(String,nullable=False)
    explanation=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")
    
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False)
    name=Column(String,nullable=False)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    phone_number=Column(String,nullable=True)
    
class Libary(Base):
    __tablename__="libarys"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    book_id=Column(Integer,ForeignKey("books.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    
    
