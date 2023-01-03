from fastapi import HTTPException,status

def Exception_id_not_found(item_name):
    item_name = item_name
    raise HTTPException(
            status_code=404,
            detail=f"This {item_name} id is not found in our database. pls enter any correct {item_name} id",
        )

def Exception_database_error():
    raise HTTPException(
        status_code=502, 
        detail="Database error"
    )

def No_book_availabe_still():
    raise HTTPException(
        status_code=404,
        detail="Again your book is not available we will text you when it is available"
    )

def HTTP_401_UNAUTHORIZED(detail):
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

def IntegrityError(status_code,detail):
    raise HTTPException(status_code=status_code, detail=detail)