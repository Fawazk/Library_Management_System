from fastapi import FastAPI, Depends, APIRouter, HTTPException

router = APIRouter(tags=["book"], prefix="/book")


@router.get("/")
async def root():
    return {"message": "Hello World"}
