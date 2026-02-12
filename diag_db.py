from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_diag():
    tables = ['users', 'chat_sessions', 'chat_history', 'chat_message']
    with engine.connect() as conn:
        print("--- DB DIAGNOSTIC ---")
        for table in tables:
            try:
                res = conn.execute(text(f"SELECT count(*) FROM {table}"))
                count = res.scalar()
                print(f"Table '{table}': {count} rows")
                if count > 0:
                    res = conn.execute(text(f"SELECT * FROM {table} LIMIT 1"))
                    print(f"  Sample row from {table}: {res.fetchone()}")
            except Exception as e:
                print(f"Error checking {table}: {e}")

if __name__ == "__main__":
    run_diag()
