from fastapi import FastAPI, Depends, APIRouter, HTTPException

router = APIRouter(tags=["class room"],prefix="/class_room")


@router.get("/")
async def root():
    return {"message": "Hello World"}
