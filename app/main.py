from fastapi import  FastAPI
from database import engin
import models
from routers import user,book,auth,libary
models.Base.metadata.create_all(bind=engin)
from config import settings

app=FastAPI()

app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(libary.router)
    