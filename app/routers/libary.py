from fastapi import APIRouter,Depends,status,HTTPException,Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2,models,schemas

router=APIRouter(prefix="/libary",tags=["libary"])

    
    

@router.get("/{book_id}")
def hasLibarys(book_id:int,current_user:schemas.UserOut=Depends(oauth2.get_current_user),dp:Session=Depends(get_db)):
    hasBook = dp.query(models.Book).filter(models.Book.id==book_id)
    if not hasBook.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return dp.query(models.Libary).filter(models.Libary.book_id==book_id,models.Libary.user_id==current_user.id).first()!=None
    

@router.post("")
def libary(book:schemas.libary,current_user:schemas.UserOut=Depends(oauth2.get_current_user),dp:Session=Depends(get_db)):
    user_id=current_user.id
    book_id=book.book_id
    hasBook = dp.query(models.Book).filter(models.Book.id==book_id)
    
    if not hasBook.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    hasLibary = dp.query(models.Libary).filter(models.Libary.book_id==book_id,models.Libary.user_id==current_user.id)
    if hasLibary.first():
        hasLibary.delete(synchronize_session=False)
        dp.commit()
        return Response(status_code=status.HTTP_200_OK)
    new_libary=models.Libary(book_id=book_id,user_id=user_id)
    dp.add(new_libary)
    dp.commit()
    return Response(status_code=status.HTTP_201_CREATED)
        
    
    
    
    
    