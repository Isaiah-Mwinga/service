from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.database import SessionLocal
import httpx
import os

# OpenID Connect provider (e.g., Auth0, Google, Keycloak)
OPENID_PROVIDER_URL = os.getenv("OPENID_PROVIDER_URL", "https://auth.example.com")

# OAuth2 settings
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{OPENID_PROVIDER_URL}/authorize",
    tokenUrl=f"{OPENID_PROVIDER_URL}/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate OpenID token and fetch user info from the provider"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{OPENID_PROVIDER_URL}/userinfo", headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    return response.json()  # Returns the authenticated user info

def get_db():
    """Dependency to get a new database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()