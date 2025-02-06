from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.database import SessionLocal
import httpx

# Load environment variables from a .env file
from dotenv import load_dotenv
import os

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# OpenID Connect provider (e.g., Auth0, Google, Keycloak)
OPENID_PROVIDER_URL = os.getenv("OPENID_PROVIDER_URL", "").strip("/")
AUTH0_AUDIENCE = os.getenv(
    "AUTH0_AUDIENCE", "https://dev-mxpkj7s8kou08yby.us.auth0.com/api/v2/"
)
USERINFO_URL = f"{OPENID_PROVIDER_URL}/userinfo"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{OPENID_PROVIDER_URL}/authorize",
    tokenUrl=f"{OPENID_PROVIDER_URL}/oauth/token",
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate OpenID token and fetch user info"""

    if not token:
        raise HTTPException(status_code=401, detail="No authentication token provided")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            USERINFO_URL, headers={"Authorization": f"Bearer {token}"}
        )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user_info = response.json()

    if "sub" not in user_info:
        raise HTTPException(status_code=403, detail="Invalid user information")

    return user_info


def get_db():
    """Dependency to get a new database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
