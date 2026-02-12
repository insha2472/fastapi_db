import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)

def verify_db():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"--- DATABASE TABLES FOUND ({len(tables)}) ---")
    
    with engine.connect() as conn:
        for table in tables:
            try:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"Table: {table:25} | Rows: {count}")
            except Exception as e:
                print(f"Table: {table:25} | Error reading: {e}")

if __name__ == "__main__":
    verify_db()
