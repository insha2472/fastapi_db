import time
from sqlalchemy import text
from db import engine, SessionLocal
from models import User

def benchmark():
    print("🚀 Starting Database Benchmark...")
    
    # 1. Measurement of connection time
    start_time = time.time()
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        conn_time = time.time() - start_time
        print(f"⏱️  Connection Establishment: {conn_time:.4f}s")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # 2. Measurement of simple query time
    session = SessionLocal()
    start_time = time.time()
    user_count = session.query(User).count()
    query_time = time.time() - start_time
    print(f"⏱️  Query Time (Count Users): {query_time:.4f}s")
    print(f"📊 Total Users: {user_count}")
    
    # 3. Measurement of filter query time
    start_time = time.time()
    user = session.query(User).filter(User.email != "nonexistent@example.com").first()
    filter_time = time.time() - start_time
    print(f"⏱️  Query Time (Filter First): {filter_time:.4f}s")
    
    session.close()
    
    total_time = conn_time + query_time + filter_time
    print(f"\n✨ Benchmark Complete! Total DB interaction time measured: {total_time:.4f}s")

if __name__ == "__main__":
    benchmark()
