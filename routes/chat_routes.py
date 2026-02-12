from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from repositories.chat_repo import ChatRepo
from schemas.chat_schemas import ChatHistory, ChatHistoryCreate, ChatMessage, ChatMessageCreate, ChatHistoryList
from utils.jwt_handler import verify_token

router = APIRouter(prefix="/chat", tags=["chat"])

# Helper to get user_id from token manually
def get_user_id_from_header(authorization: str = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.get("/history", response_model=List[ChatHistoryList])
def get_history(authorization: str = None, db: Session = Depends(get_db)):
    user_id = get_user_id_from_header(authorization)
    repo = ChatRepo(db)
    return repo.get_history_by_user(user_id)

@router.post("/history", response_model=ChatHistory)
def create_history(history: ChatHistoryCreate, authorization: str = None, db: Session = Depends(get_db)):
    user_id = get_user_id_from_header(authorization)
    repo = ChatRepo(db)
    return repo.create_history(user_id, history)

@router.get("/history/{history_id}/messages", response_model=List[ChatMessage])
def get_messages(history_id: int, authorization: str = None, db: Session = Depends(get_db)):
    # Verify history belongs to user
    user_id = get_user_id_from_header(authorization)
    repo = ChatRepo(db)
    history = repo.get_history(history_id)
    if not history or history.user_id != user_id:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return repo.get_messages_by_history(history_id)

@router.post("/history/{history_id}/messages", response_model=ChatMessage)
def add_message(history_id: int, message: ChatMessageCreate, authorization: str = None, db: Session = Depends(get_db)):
    user_id = get_user_id_from_header(authorization)
    repo = ChatRepo(db)
    history = repo.get_history(history_id)
    if not history or history.user_id != user_id:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return repo.add_message(history_id, message)
