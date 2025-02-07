from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2AuthorizationCodeBearer
import os

import uvicorn
from app import database
from app.routes import customers, orders, auth
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

app = FastAPI(title="Customer Order API")

# OpenID Config
OPENID_PROVIDER_URL = os.getenv("OPENID_PROVIDER_URL", "").strip("/")
TOKEN_URL = f"{OPENID_PROVIDER_URL}/oauth/token"
AUTH_URL = f"{OPENID_PROVIDER_URL}/authorize"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTH_URL, tokenUrl=TOKEN_URL
)


# Fix Swagger UI Authentication
def custom_openapi():
    if not app.openapi_schema:
        openapi_schema = get_openapi(
            title="Customer Order API",
            version="1.0.0",
            description="API documentation with OpenID authentication & SSO",
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "OAuth2": {
                "type": "oauth2",
                "flows": {
                    "authorizationCode": {
                        "authorizationUrl": AUTH_URL,
                        "tokenUrl": TOKEN_URL,
                        "scopes": {},
                    }
                },
            }
        }
        openapi_schema["security"] = [{"OAuth2": []}]
        app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# CORS Middleware (Allow OpenID Requests)
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


# Ensure database is initialized
database.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use Render's assigned PORT
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
