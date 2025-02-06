import os
from dotenv import load_dotenv

# Explicitly load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

print("🔍 DEBUG: Checking Environment Variables...")

env_vars = [
    "OPENID_PROVIDER_URL",
    "AUTH0_AUDIENCE",
    "CLIENT_ID",
    "CLIENT_SECRET",
    "REDIS_URL",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
]

for var in env_vars:
    print(f"{var}: {os.getenv(var)}")
