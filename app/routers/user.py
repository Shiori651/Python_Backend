


from fastapi import Depends, FastAPI, HTTPException,Response,status,APIRouter
from typing import List
from sqlalchemy.orm import Session 
from .. import schemas,models, utils

from typing import List
from app.database import get_dp
router=APIRouter(
    prefix="/user",
    tags=["User"])



@router.get("",response_model=List[schemas.UserOut])
def get_user(dp:Session=Depends(get_dp)):
    users=dp.query(models.User).offset(0).limit(10).all()
    return users

@router.post("",response_model=schemas.UserOut,status_code=201)
def creat_user(user:schemas.UserCreat,dp:Session=Depends(get_dp)):
    
    user_has=dp.query(models.User).filter(models.User.email==user.email).first()
    if user_has is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    user.password=utils.hash(user.password)
    new_user=models.User(**user.model_dump())
    dp.add(new_user)
    dp.commit()
    dp.refresh(new_user)
    
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def search_user(id:int,db:Session=Depends(get_dp)): 
    searched_user=db.query(models.User).filter(models.User.id==id)
    if(searched_user.first() is None):
        raise HTTPException(status_code=404)
    return searched_user.first()

@router.delete("/{id}",status_code=204)
def delete_user(id:int,dp:Session=Depends(get_dp)):
    deleted_user=dp.query(models.User).filter(models.User.id==id)
    if(deleted_user.first() is None):
        raise HTTPException(status_code=404)
    dp.delete(deleted_user.first())
    dp.commit()
    return 
