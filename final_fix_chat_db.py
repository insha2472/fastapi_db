import os
from dotenv import load_dotenv
load_dotenv()

from db import engine, SessionLocal, Base
from models import User, ChatHistory, ChatMessage
from datetime import datetime

def setup_chat_in_db():
    # 1. Ensure tables are created in the current DB
    print("DEBUG: Creating tables (chat_history, chat_messages)...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 2. Get or create a sample user to attach history to
        print("DEBUG: Checking for user...")
        user = db.query(User).first()
        if not user:
            user = User(email="deployment_tester@example.com", password="dummy_password")
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"DEBUG: Created new user with ID: {user.id}")
        else:
            print(f"DEBUG: Using existing user with ID: {user.id}")

        # 3. Clear any existing content in these specific tables
        print("DEBUG: Clearing existing history data...")
        db.query(ChatMessage).delete()
        db.query(ChatHistory).delete()
        db.commit()

        # 4. Populate with real session history
        print("DEBUG: Populating session history...")
        
        # Topic 1: Database Setup
        h1 = ChatHistory(title="Setup: Missing User Table", user_id=user.id)
        db.add(h1)
        db.flush()
        db.add(ChatMessage(history_id=h1.id, role="user", content="why my test.db is not showing user table"))
        db.add(ChatMessage(history_id=h1.id, role="assistant", content="We found you were using Aiven PostgreSQL. I initialized the remote tables and verified the connection."))

        # Topic 2: Deployment
        h2 = ChatHistory(title="Fix: Render Deployment", user_id=user.id)
        db.add(h2)
        db.flush()
        db.add(ChatMessage(history_id=h2.id, role="user", content="i cant deploy (requirements.txt not found)"))
        db.add(ChatMessage(history_id=h2.id, role="assistant", content="Moved files to repo root and added render.yaml to fix the 'unicorn' vs 'uvicorn' typo."))

        db.commit()
        print("SUCCESS: Chat history successfully saved to PostgreSQL!")

    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    setup_chat_in_db()
