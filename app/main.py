from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.routers import user,book,auth,libary
from .config import settings

app=FastAPI()
origins =["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(libary.router)

@app.get("/")
def root():
   return{"message:":"Seni Seviyorum Bebeğim <3"}

@app.get("/sena")
def root():
   return{"message:":"Seni Seviyorum Bebeğim <3"}