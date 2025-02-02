# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer
import os
from app import database
from app.routes import customers, orders, auth



app = FastAPI(title="Customer Order API")

# OpenID Connect configuration
OPENID_PROVIDER_URL = os.getenv("OPENID_PROVIDER_URL", "https://dev-xxxxx.auth0.com")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{OPENID_PROVIDER_URL}/authorize",
    tokenUrl=f"{OPENID_PROVIDER_URL}/oauth/token"
)

# Correct OpenAPI security definition using a dictionary
security_scheme = {
    "OAuth2": {
        "type": "oauth2",
        "flows": {
            "authorizationCode": {
                "authorizationUrl": f"{OPENID_PROVIDER_URL}/authorize",
                "tokenUrl": f"{OPENID_PROVIDER_URL}/oauth/token"
            }
        }
    }
}

# Add security scheme to OpenAPI documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = app.openapi()
    openapi_schema["components"]["securitySchemes"] = security_scheme
    openapi_schema["security"] = [{"OAuth2": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.get("/")
def root():
    return {"message": "Welcome to the Customer Order API"}

# Database Initialization
database.Base.metadata.create_all(bind=database.engine)
