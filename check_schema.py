import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text

engine = create_engine(os.getenv("DATABASE_URL"))

def check_schema_visibility():
    query = text("""
        SELECT table_schema, table_name 
        FROM information_schema.tables 
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name;
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query)
        print("--- ACCESSIBLE TABLES BY SCHEMA ---")
        for row in result:
            print(f"Schema: {row[0]:15} | Table: {row[1]}")

if __name__ == "__main__":
    check_schema_visibility()
