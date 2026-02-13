import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env file.")
    sys.exit(1)

print(f"Testing connection to: {DATABASE_URL.split('@')[-1]}") # Mask credentials

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()
        print(f"Successfully connected! PostgreSQL version: {version[0]}")
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)
