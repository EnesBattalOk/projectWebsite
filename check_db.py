import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('instance/projects.db')
        cursor = conn.cursor()
        
        print("--- Projects ---")
        cursor.execute("SELECT name, slug, is_default FROM project")
        for row in cursor.fetchall():
            print(f"Project: {row[0]}, Slug: {row[1]}, Default: {row[2]}")
            
        print("\n--- News ---")
        cursor.execute("SELECT title, project_id FROM news")
        for row in cursor.fetchall():
            print(f"News: {row[0]}, Project ID: {row[1]}")
            
        print("\n--- Users ---")
        cursor.execute("SELECT username FROM user")
        for row in cursor.fetchall():
            print(f"User: {row[0]}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
