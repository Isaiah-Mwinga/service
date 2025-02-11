from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from app import database
from app.routes import customers, orders

app = FastAPI(title="Customer Order API")

# CORS Middleware (Allow OpenID Requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
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
