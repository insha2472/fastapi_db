from sqlalchemy.orm import Session
from models import ChatHistory, ChatMessage
from schemas.chat_schemas import ChatHistoryCreate, ChatMessageCreate

class ChatRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_history_by_user(self, user_id: int):
        return self.db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.created_at.desc()).all()

    def get_history(self, history_id: int):
        return self.db.query(ChatHistory).filter(ChatHistory.id == history_id).first()

    def create_history(self, user_id: int, history: ChatHistoryCreate):
        db_history = ChatHistory(user_id=user_id, title=history.title)
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def add_message(self, history_id: int, message: ChatMessageCreate):
        db_message = ChatMessage(history_id=history_id, role=message.role, content=message.content)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_messages_by_history(self, history_id: int):
        return self.db.query(ChatMessage).filter(ChatMessage.history_id == history_id).all()
