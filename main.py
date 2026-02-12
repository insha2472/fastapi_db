from fastapi import FastAPI
from routes.user_routes import router as user_routes
from db import get_db, engine
from models import Base
from routes.email_routes import router as email_routes
from routes.ai_response_routes import router as ai_response_routes
from routes.chat_routes import router as chat_routes
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes)
app.include_router(email_routes)
app.include_router(ai_response_routes)
app.include_router(chat_routes)

# Create database tables
Base.metadata.create_all(bind=engine)
print(f"✅ Successfully connected to Postgres Database: {engine.url.host}")

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)