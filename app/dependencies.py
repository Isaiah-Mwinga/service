from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    SecurityScopes,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from app.config import get_settings
from app.database import SessionLocal


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires authentication",
        )


class VerifyToken:
    """Handles token verification using PyJWT"""

    def __init__(self):
        self.config = get_settings()

        # Get JWKS from Auth0
        jwks_url = f"https://{self.config.AUTH0_DOMAIN}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ):
        if token is None:
            raise UnauthenticatedException()

        # Validate the token signature
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except (
            jwt.exceptions.PyJWKClientError,
            jwt.exceptions.DecodeError,
        ) as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=[self.config.AUTH0_ALGORITHMS],
                audience=self.config.AUTH0_API_AUDIENCE,
                issuer=self.config.AUTH0_ISSUER,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))

        # Check if required scopes exist in the token
        if security_scopes.scopes:
            self._check_claims(payload, "scope", security_scopes.scopes)

        return payload

    def _check_claims(self, payload, claim_name, expected_values):
        """Check if the token contains the required claims"""
        if claim_name not in payload:
            raise UnauthorizedException(
                f'No claim "{claim_name}" found in token'
            )

        payload_claim = payload[claim_name]
        if claim_name == "scope":
            payload_claim = payload_claim.split(" ")

        for value in expected_values:
            if value not in payload_claim:
                raise UnauthorizedException(
                    f'Missing "{claim_name}" scope: {value}'
                )


# ✅ Create a single instance of VerifyToken to reuse across routes
verify_token = VerifyToken()


# Dependency to get a new database session
def get_db():
    """Get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
