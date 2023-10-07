from fastapi import APIRouter,Depends,status,HTTPException,Response
from database import get_dp
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import func
import schemas,models,utils,oauth2
router=APIRouter(tags=["Authentication"])
from typing import List

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), dp:Session=Depends(get_dp)):

    
    user= dp.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not  user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
    access_token = oauth2.creat_access_token(data={"user_id":user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}
