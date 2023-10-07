from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import schemas,models
from config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

from database import get_dp
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def creat_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentionals_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        id:str=payload.get("user_id")
        if id is None:
            raise credentionals_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentionals_exception
    return token_data

def get_current_user(token:str =Depends(oauth2_scheme),dp:Session=Depends(get_dp)):
    credentionals_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token_data=verify_access_token(token,credentionals_exception)
    
    user=dp.query(models.User).filter(models.User.id==token_data.id).first()
    if user is None:
        raise credentionals_exception
    return user