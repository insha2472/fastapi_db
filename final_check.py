import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine, text

engine = create_engine(os.getenv("DATABASE_URL"))
with engine.connect() as conn:
    res = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
    print([r[0] for r in res])
