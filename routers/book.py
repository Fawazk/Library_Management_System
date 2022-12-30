

from fastapi import FastAPI, Depends, APIRouter, HTTPException
from models.pydantic_models.request.book import BookRequest
from models.pydantic_models.response.book import BookResponse
from config.database import get_db
from sqlmodel import Session
from operations import book as functions



router = APIRouter(tags=["book"], prefix="/book")


@router.post("/register-book", response_model=BookResponse)
async def register_book(book_data: BookRequest, db: Session = Depends(get_db)):
    """To register the book"""
    response = functions.register_book(db, book_data)
    return response
    

@router.get("/list-books", response_model=list[BookResponse])
async def get_book(
    skip:int = 0,
    limit:int = 100,
    db: Session = Depends(get_db),
):
    """To get one book by the id given"""
    response = functions.get_book(db=db,skip=skip,limit=limit)
    return response


@router.get("/get-book", response_model=BookResponse)
async def get_books(
    book_id: int,
    db: Session = Depends(get_db),
):
    """To get one book by the id given"""
    response = functions.get_book(db=db,book_id=book_id)
    return response