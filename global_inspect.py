from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_all_tables():
    with engine.connect() as conn:
        print("--- All Tables (Global Search) ---")
        res = conn.execute(text("""
            SELECT schemaname, tablename 
            FROM pg_catalog.pg_tables 
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        """))
        for row in res:
            print(f"Schema: {row[0]}, Table: {row[1]}")
            # Count rows
            count_res = conn.execute(text(f"SELECT count(*) FROM {row[0]}.{row[1]}"))
            print(f"  Count: {count_res.scalar()}")

if __name__ == "__main__":
    check_all_tables()
