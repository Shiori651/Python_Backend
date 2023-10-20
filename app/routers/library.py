from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.responses import JSONResponse
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2,models,schemas    

router = APIRouter(prefix="/library",tags=["Library"])

    
    

@router.get("/{book_id}")
def hasLibrarys(book_id:int,current_user:schemas.UserOut=Depends(oauth2.get_current_user),db:Session=Depends(get_db)):
    hasBook = db.query(models.Book).filter(models.Book.id==book_id)
    if not hasBook.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db.query(models.Library).filter(models.Library.book_id==book_id,models.Library.user_id==current_user.id).first()!=None
    

@router.post("")
def library(book:schemas.library,current_user:schemas.UserOut=Depends(oauth2.get_current_user),db:Session=Depends(get_db)):
    user_id=current_user.id
    book_id=book.book_id
    hasBook = db.query(models.Book).filter(models.Book.id==book_id)
    
    if not hasBook.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    library_query = db.query(models.Library).filter(models.Library.book_id == book_id, models.Library.user_id == current_user.id)
    hasLibrary=library_query.first()
    if book.dir == 1:
        if hasLibrary:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        new_library=models.Library(book_id=book_id, user_id=user_id)
        db.add(new_library)
        db.commit()
        return JSONResponse(content="Successfuly Add Created",status_code=201)
    else :
        if not hasLibrary:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        library_query.delete(synchronize_session=False)
        db.commit()
        return JSONResponse(content="Successfuly delete Created",status_code=200)

    
    