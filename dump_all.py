from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def dump_data():
    tables = ['chat_sessions', 'chat_history', 'chat_message', 'chat_messages']
    with engine.connect() as conn:
        for table in tables:
            print(f"\n--- Data in {table} ---")
            try:
                res = conn.execute(text(f"SELECT * FROM {table}"))
                for row in res:
                    print(row)
            except Exception as e:
                print(f"Error reading {table}: {e}")

if __name__ == "__main__":
    dump_data()
