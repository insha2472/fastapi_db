from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def inspect_db():
    with engine.connect() as conn:
        print("--- Tables ---")
        res = conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"))
        tables = [r[0] for r in res]
        print(f"Tables: {tables}")
        
        for table in tables:
            print(f"\n--- {table} (last 5 rows) ---")
            try:
                res = conn.execute(text(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 5"))
                for row in res:
                    print(row)
            except Exception as e:
                print(f"Error reading {table}: {e}")

if __name__ == "__main__":
    inspect_db()
