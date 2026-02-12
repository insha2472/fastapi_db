import time
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"Testing connection to: {DATABASE_URL}")

start_time = time.time()
engine = create_engine(DATABASE_URL)
try:
    with engine.connect() as connection:
        end_connect_time = time.time()
        print(f"Connection established in: {end_connect_time - start_time:.4f} seconds")
        
        result = connection.execute(text("SELECT 1"))
        end_query_time = time.time()
        print(f"Query executed in: {end_query_time - end_connect_time:.4f} seconds")
        print(f"Total time: {end_query_time - start_time:.4f} seconds")
except Exception as e:
    print(f"Connection failed: {e}")
