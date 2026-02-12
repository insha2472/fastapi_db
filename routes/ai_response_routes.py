from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from utils.ai_response import get_completion
from schemas.ai_response_schemas import AIRequest, AIResponse
from repositories.chat_repo import ChatRepo
from schemas.chat_schemas import ChatMessageCreate, ChatHistoryCreate
from utils.jwt_handler import verify_token
from fastapi import Header

router = APIRouter()


@router.post("/ask", response_model=AIResponse)
def ask_ai(request: AIRequest, authorization: str = Header(None), db: Session = Depends(get_db)):
    """Get response from AI model and save to history if authorized."""
    try:
        response_text = get_completion(request.message, request.system_prompt)
        
        # Determine user_id from token if available
        user_id = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            payload = verify_token(token)
            if payload:
                user_id = int(payload.get("sub"))
        
        # If we have a user, save the interaction
        if user_id:
            repo = ChatRepo(db)
            # Find or create a default 'AI Chat' history for this interactive mode
            histories = repo.get_history_by_user(user_id)
            if histories:
                history = histories[0] # Use the most recent
            else:
                history = repo.create_history(user_id, ChatHistoryCreate(title="AI Chat"))
            
            # Save user message
            repo.add_message(history.id, ChatMessageCreate(role="user", content=request.message))
            # Save assistant response
            repo.add_message(history.id, ChatMessageCreate(role="assistant", content=response_text))

        return AIResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))