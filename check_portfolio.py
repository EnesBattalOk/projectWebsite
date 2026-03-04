import sqlite3
import json

def check_portfolio_db():
    try:
        conn = sqlite3.connect('c:/Users/enesb/Desktop/projects/zip-repl/zip/portfolio (3).db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        # Check water saving entries if the table exists
        if ('water_saving_entry',) in tables:
            cursor.execute("SELECT * FROM water_saving_entry LIMIT 1")
            row = cursor.fetchone()
            print(f"Sample Entry: {row}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_portfolio_db()
