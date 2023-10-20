
from fastapi import Depends, HTTPException,Response,status,APIRouter
from typing import List, cast
from sqlalchemy import Integer, func
from sqlalchemy.orm import Session 
from .. import schemas,models,oauth2
from ..database  import get_db
from typing import Optional

router=APIRouter(prefix="/book",tags=["Book"])

@router.get("",response_model=List[schemas.BookOut])
def get_book(db:Session=Depends(get_db),curret_user:schemas.UserOut=Depends(oauth2.get_current_user),
             limit:int =10,skip:int=0,search:Optional[str]=""):
    # books=db.query(models.Book).filter(models.Book.owner_id==curret_user.id).filter(models.Book.name.contains(search)).\
    #     limit(limit).offset(skip).all()

    # if books is None:
    #     raise HTTPException(status_code=404)
    deneme=db.query(models.Book,func.count(models.Library.book_id).label("laybarys"))\
        .join(models.Library,models.Library.book_id==models.Book.id,isouter=True).filter(models.Book.owner_id==curret_user.id).\
            group_by(models.Book.id).filter(models.Book.name.contains(search)).limit(limit).offset(skip).all()
    return deneme


@router.post("",response_model=schemas.Book,status_code=201)
def creat_book(book:schemas.BookCreate,db:Session=Depends(get_db), curret_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    new_book=models.Book(owner_id=curret_user.id,**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/{isbn}",response_model=schemas.BookOut)
def search_book(isbn:str,db:Session=Depends(get_db)):
    searched_book=db.query(models.Book,func.count(models.Library.book_id).label("laybarys"))\
        .join(models.Library,models.Library.book_id==models.Book.id,isouter=True).filter(models.Book.isbn==isbn).\
            group_by(models.Book.id).filter(models.Book.isbn==isbn).first()
    if searched_book is None :
        raise HTTPException(status_code= 404,detail="Book not found")
    return searched_book


@router.delete("/{id}")
def delete_book(id:int, db:Session=Depends(get_db), curret_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    book=db.query(models.Book).filter(models.Book.id==id)
    isbook=book.first()
    
    if isbook == None:
        raise HTTPException(status_code= 404,detail="Book not found")
    
    if  isbook.owner_id!=curret_user.id:
        raise HTTPException(status_code= 403)

    book.delete(synchronize_session= False)
    db.commit() 
    return Response(status_code=204)


@router.put("/{id}",response_model=schemas.Book)
def update_book(id:int,book:schemas.BookCreate ,db:Session=Depends(get_db), curret_user:schemas.UserOut=Depends(oauth2.get_current_user)):
    book_query= db.query(models.Book).filter(models.Book.id==id)
    update_book=book_query.first()
    
    if update_book == None:
        raise HTTPException(status_code=404)
        
    if update_book.owner_id!=curret_user.id:
         raise HTTPException(status_code= 403)
     
    book_query.update(book.model_dump(),synchronize_session=False)
    db.commit()
    return book_query.first()