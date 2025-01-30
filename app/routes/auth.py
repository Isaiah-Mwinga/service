from fastapi import APIRouter, Depends
from app.schemas import Token
from app.dependencies import oauth2_scheme

router = APIRouter()

@router.get("/login", response_model=Token)
def login(token: str = Depends(oauth2_scheme)):
    return {"access_token": token, "token_type": "bearer"}
