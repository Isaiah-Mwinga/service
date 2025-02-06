from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/userinfo")
async def get_user_info(user: dict = Depends(get_current_user)):
    """Fetch authenticated user details"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
