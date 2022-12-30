from fastapi import HTTPException

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