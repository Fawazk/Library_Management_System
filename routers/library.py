from fastapi import FastAPI, Depends, APIRouter, HTTPException

router = APIRouter(tags=["library"],prefix="/library")


@router.get("/")
async def root():
    return {"message": "Hello World"}
