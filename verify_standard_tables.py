import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, inspect, text

engine = create_engine(os.getenv("DATABASE_URL"))

def verify_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in DB: {tables}")
    
    if "chat_history" in tables:
        print("SUCCESS: 'chat_history' table exists.")
        with engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM chat_history")).scalar()
            print(f"Rows in chat_history: {count}")
    else:
        print("FAIL: 'chat_history' table does NOT exist.")

if __name__ == "__main__":
    verify_tables()
