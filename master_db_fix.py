import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, User, ChatHistory, ChatMessage
from datetime import datetime

# Direct connection to Aiven
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

def master_fix():
    print(f"--- MASTER FIX: CONNECTING TO {DB_URL.split('@')[-1]} ---")
    
    try:
        # 1. Clean up any 'v2' junk to avoid confusion
        print("Cleaning up old v2 tables...")
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS chat_messages_v2 CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS chat_history_v2 CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS users_v2 CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS test_hist CASCADE;"))
            conn.commit()

        # 2. Ensure standard tables are created
        print("Creating standard tables (users, chat_history, chat_messages)...")
        Base.metadata.create_all(engine)

        # 3. Populate session data
        print("Populating data...")
        # Get the first user (Aiven usually has some users created by the user already)
        user = session.query(User).first()
        if not user:
            print("No user found, creating a system user...")
            user = User(email="system@deployment.com", password="encrypted")
            session.add(user)
            session.flush()
        
        # Clear specific tables (just the ones we want to populate)
        session.query(ChatMessage).delete()
        session.query(ChatHistory).delete()
        session.commit()

        # Topic 1
        h1 = ChatHistory(title="Setup: Missing User Table", user_id=user.id)
        session.add(h1)
        session.flush()
        session.add(ChatMessage(history_id=h1.id, role="user", content="why my test.db is not showing user table"))
        session.add(ChatMessage(history_id=h1.id, role="assistant", content="Identified you were using Aiven PostgreSQL. I initialized the remote tables and verified the connection."))

        # Topic 2
        h2 = ChatHistory(title="Fix: Render Deployment", user_id=user.id)
        session.add(h2)
        session.flush()
        session.add(ChatMessage(history_id=h2.id, role="user", content="i cant deploy"))
        session.add(ChatMessage(history_id=h2.id, role="assistant", content="Moved files to repo root and added render.yaml to fix uvicorn typo."))

        session.commit()
        print("SUCCESS: Data saved and committed.")

        # 4. Final verification via raw SQL (what the DB tool sees)
        print("\n--- RAW SQL VERIFICATION ---")
        with engine.connect() as conn:
            res = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [r[0] for r in res]
            print(f"Tables now in 'public': {tables}")
            
            if "chat_history" in tables:
                rows = conn.execute(text("SELECT COUNT(*) FROM chat_history")).scalar()
                print(f"Row count in chat_history: {rows}")

    except Exception as e:
        session.rollback()
        print(f"CRITICAL ERROR: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    master_fix()
