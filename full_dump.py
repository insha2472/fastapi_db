from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def dump_all():
    with engine.connect() as conn:
        print("--- CHAT_HISTORY ---")
        res = conn.execute(text("SELECT * FROM chat_history"))
        for row in res:
            print(row)
        
        print("\n--- CHAT_MESSAGE ---")
        res = conn.execute(text("SELECT * FROM chat_message"))
        for row in res:
            print(row)

if __name__ == "__main__":
    dump_all()
