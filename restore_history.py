from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import Base, User, ChatSession, ChatHistory, ChatMessage
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def sync_schema():
    print("--- Syncing Database Schema (FIX) ---")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Get the first user
        user = db.query(User).first()
        if not user:
            print("No user found. Creating dummy user...")
            user = User(email="insha24@gmail.com", name="insha", password="password123")
            db.add(user)
            db.flush()

        print(f"Using User ID={user.id}")

        # Create a session
        session = ChatSession(user_id=user.id)
        db.add(session)
        db.flush()
        print(f"Created Session ID={session.id}")

        # 1. Topic: Database Migration
        h1 = ChatHistory(title="Database Migration & Sync", user_id=user.id, session_id=session.id)
        db.add(h1)
        db.flush()
        print(f"Created History ID={h1.id}")
        
        db.add(ChatMessage(history_id=h1.id, role="user", content="Sync my chat history to chat_history, chat_message and chat_sessions"))
        db.add(ChatMessage(history_id=h1.id, role="assistant", content="Modified models.py to rename chat_messages to chat_message and added ChatSession model linked to chat_sessions table."))

        # 2. Topic: Previous Session Work
        h2 = ChatHistory(title="Fixing Errors & Optimization", user_id=user.id, session_id=session.id)
        db.add(h2)
        db.flush()
        print(f"Created History ID={h2.id}")
        
        db.add(ChatMessage(history_id=h2.id, role="user", content="Fix the 'main' module error and jose syntax errors"))
        db.add(ChatMessage(history_id=h2.id, role="assistant", content="Identified global 'jose' package conflict. Uninstalled legacy package, reinstalled modern python-jose, and moved files to root to fix import paths."))

        db.commit()
        print("SUCCESS: Database schema synced and chat history populated.")

        # FINAL CHECK inside script
        count = db.query(ChatHistory).count()
        print(f"Final ChatHistory count: {count}")

    except Exception as e:
        db.rollback()
        print(f"FAILURE: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    sync_schema()
