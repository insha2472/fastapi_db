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
    print("--- Syncing Database Schema ---")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Get the first user
        print("DEBUG: Checking for user...")
        user = db.query(User).first()
        if not user:
            print("No user found. Please sign up or create a user first.")
            return

        print(f"DEBUG: Using User ID={user.id}")

        # Create a session
        print("DEBUG: Creating a new chat session...")
        session = ChatSession(user_id=user.id)
        db.add(session)
        db.flush()

        # 1. Topic: Database Migration
        print("DEBUG: Populating Topic 1 (Database Migration)...")
        h1 = ChatHistory(title="Database Migration & Sync", user_id=user.id, session_id=session.id)
        db.add(h1)
        db.flush()
        
        db.add(ChatMessage(history_id=h1.id, role="user", content="Sync my chat history to chat_history, chat_message and chat_sessions"))
        db.add(ChatMessage(history_id=h1.id, role="assistant", content="Modified models.py to rename chat_messages to chat_message and added ChatSession model linked to chat_sessions table."))

        # 2. Topic: Previous Session Work
        print("DEBUG: Populating Topic 2 (Previous Session Work)...")
        h2 = ChatHistory(title="Fixing Errors & Optimization", user_id=user.id, session_id=session.id)
        db.add(h2)
        db.flush()
        
        db.add(ChatMessage(history_id=h2.id, role="user", content="Fix the 'main' module error and jose syntax errors"))
        db.add(ChatMessage(history_id=h2.id, role="assistant", content="Identified global 'jose' package conflict. Uninstalled legacy package, reinstalled modern python-jose, and moved files to root to fix import paths."))

        db.commit()
        print("SUCCESS: Database schema synced and chat history populated.")

    except Exception as e:
        db.rollback()
        print(f"FAILURE: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    sync_schema()
