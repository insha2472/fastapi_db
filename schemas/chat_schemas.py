from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChatMessageBase(BaseModel):
    role: str
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    history_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistoryBase(BaseModel):
    title: str

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistory(ChatHistoryBase):
    id: int
    user_id: int
    created_at: datetime
    messages: List[ChatMessage] = []

    class Config:
        from_attributes = True

class ChatHistoryList(ChatHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
