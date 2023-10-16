


from fastapi import Depends, FastAPI, HTTPException,Response,status,APIRouter
from typing import List
from sqlalchemy.orm import Session 
from .. import schemas,models, utils

from typing import List
from ..database import get_db
router=APIRouter(
    prefix="/user",
    tags=["User"])



@router.get("",response_model=List[schemas.UserOut])
def get_user(dp:Session=Depends(get_db)):
    users=dp.query(models.User).offset(0).limit(10).all()
    return users

@router.post("",response_model=schemas.UserOut,status_code=201)
def creat_user(user:schemas.UserCreat,dp:Session=Depends(get_db)):
    
    user_has=dp.query(models.User).filter(models.User.email==user.email).first()
    if user_has is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    user.password=utils.hash(user.password)
    new_user=models.User(**user.model_dump())
    dp.add(new_user)
    dp.commit()
    dp.refresh(new_user)
    
    return new_user