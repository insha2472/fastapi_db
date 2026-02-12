import sqlite3
import os

def check_sqlite(db_path):
    if not os.path.exists(db_path):
        print(f"File not found: {db_path}")
        return
    
    print(f"\n--- Checking {db_path} ---")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        print(f"Tables: {tables}")
        
        for table in tables:
            cursor.execute(f"SELECT count(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Table '{table}': {count} rows")
            if count > 0:
                cursor.execute(f"SELECT * FROM {table} LIMIT 2")
                print(f"  Sample: {cursor.fetchall()}")
        
        conn.close()
    except Exception as e:
        print(f"Error checking {db_path}: {e}")

if __name__ == "__main__":
    check_sqlite("test.db")
    check_sqlite("fastapi_db/test.db")
