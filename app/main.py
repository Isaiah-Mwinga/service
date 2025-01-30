from fastapi import FastAPI, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from app import database
from app.routes import customers, orders, auth

app = FastAPI(title="Customer Order API")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://auth.example.com/authorize",
    tokenUrl="https://auth.example.com/token"
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
