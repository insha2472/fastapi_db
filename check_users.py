from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_users():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM users"))
        print("--- Users in DB ---")
        for row in res:
            print(row)

if __name__ == "__main__":
    check_users()
