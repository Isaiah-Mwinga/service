from fastapi import Security
from fastapi.security import SecurityScopes
from app.dependencies import verify_token


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Security(verify_token.verify)
):
    """
    Extracts and returns the decoded JWT payload if the token is valid.
    """
    return token  # This is the decoded JWT payload
