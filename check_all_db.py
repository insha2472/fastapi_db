from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_all_schemas():
    with engine.connect() as conn:
        print("--- All Tables in All Schemas ---")
        res = conn.execute(text("SELECT schema_name FROM information_schema.schemata"))
        schemas = [r[0] for r in res]
        for schema in schemas:
            print(f"\nSchema: {schema}")
            res = conn.execute(text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}'"))
            for r in res:
                print(f"  Table: {r[0]}")

if __name__ == "__main__":
    check_all_schemas()
