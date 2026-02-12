from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def reset_db():
    queries = [
        "DROP TABLE IF EXISTS chat_sessions CASCADE",
        "DROP TABLE IF EXISTS chat_messages CASCADE",
        "DROP TABLE IF EXISTS chat_message CASCADE",
        "DROP TABLE IF EXISTS chat_history CASCADE",
        "DROP TABLE IF EXISTS users CASCADE"
    ]
    with engine.connect() as conn:
        for q in queries:
            try:
                conn.execute(text(q))
                print(f"Executed: {q}")
            except Exception as e:
                print(f"Error executing {q}: {e}")
        conn.commit()
    print("DB Reset (CASCADE) Complete")

if __name__ == "__main__":
    reset_db()
