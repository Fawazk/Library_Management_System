from fastapi import FastAPI, Depends, APIRouter, HTTPException

router = APIRouter(tags=["students"],prefix="/students")


@router.get("/")
async def root():
    return {"message": "Hello World"}
