from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models import Base, User, ChatSession, ChatHistory, ChatMessage
from datetime import datetime, timedelta

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def migrate_history():
    print("--- Migrating Ziggy Project History ---")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Ensure "Ziggy User" exists
        user = db.query(User).filter(User.name == "Ziggy User").first()
        if not user:
            print("Creating Ziggy User...")
            user = User(email="ziggy@example.com", name="Ziggy User", password="hashed_password_placeholder")
            db.add(user)
            db.flush()

        # 2. Create the Evolution Session
        print("Creating 'Project Evolution' Session...")
        session = ChatSession(user_id=user.id, created_at=datetime.utcnow() - timedelta(days=2))
        db.add(session)
        db.flush()

        # 3. Topic: Ziggy Rebranding
        print("Migrating: Rebranding...")
        h1 = ChatHistory(title="Ziggy Cat Rebranding", user_id=user.id, session_id=session.id, created_at=datetime.utcnow() - timedelta(days=2))
        db.add(h1)
        db.flush()
        db.add(ChatMessage(history_id=h1.id, role="user", content="I want to replace the robot logo with a cat. Let's call him Ziggy.", created_at=datetime.utcnow() - timedelta(days=2)))
        db.add(ChatMessage(history_id=h1.id, role="assistant", content="Successfully rebranded the app to Ziggy! Replaced all robot logos with the new Cat logo in the header, login/signup pages, and the dashboard avatar.", created_at=datetime.utcnow() - timedelta(days=2)))

        # 4. Topic: Feature Expansion
        print("Migrating: Feature Expansion...")
        h2 = ChatHistory(title="Markdown & AI Features", user_id=user.id, session_id=session.id, created_at=datetime.utcnow() - timedelta(days=1))
        db.add(h2)
        db.flush()
        db.add(ChatMessage(history_id=h2.id, role="user", content="Can Ziggy support markdown and generate images?", created_at=datetime.utcnow() - timedelta(days=1)))
        db.add(ChatMessage(history_id=h2.id, role="assistant", content="Yes! Implemented rich Markdown formatting and added specialized modes for Search, Study, and Image Creation. Ziggy can now generate and display beautiful visuals.", created_at=datetime.utcnow() - timedelta(days=1)))

        # 5. Topic: Dashboard Optimization
        print("Migrating: Dashboard Optimization...")
        h3 = ChatHistory(title="Dashboard & Mobile Polish", user_id=user.id, session_id=session.id, created_at=datetime.utcnow() - timedelta(hours=12))
        db.add(h3)
        db.flush()
        db.add(ChatMessage(history_id=h3.id, role="user", content="The sidebar feels clunky on mobile. Can we fix it?", created_at=datetime.utcnow() - timedelta(hours=12)))
        db.add(ChatMessage(history_id=h3.id, role="assistant", content="Optimized the dashboard for a one-page viewport and redesigned the sidebar with a smooth dropdown history list and desktop toggle for better screen use.", created_at=datetime.utcnow() - timedelta(hours=12)))

        # 6. Topic: Backend Stability
        print("Migrating: Backend Stability...")
        h4 = ChatHistory(title="Solving Startup & Import Errors", user_id=user.id, session_id=session.id, created_at=datetime.utcnow() - timedelta(minutes=30))
        db.add(h4)
        db.flush()
        db.add(ChatMessage(history_id=h4.id, role="user", content="Why am I getting a SyntaxError on startup?", created_at=datetime.utcnow() - timedelta(minutes=30)))
        db.add(ChatMessage(history_id=h4.id, role="assistant", content="Identified a conflict with a legacy 'jose' library. Cleaned up global packages, reinstalled python-jose, and moved files to the root to fix module imports.", created_at=datetime.utcnow() - timedelta(minutes=30)))

        db.commit()
        print(f"SUCCESS: Ziggy Project History migrated! User={user.name}, Session ID={session.id}")

    except Exception as e:
        db.rollback()
        print(f"FAILURE: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_history()
