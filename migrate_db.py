import sqlite3
import os

db_path = 'instance/projects.db'

def migrate():
    if not os.path.exists(db_path):
        print(f"DB not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current columns
    cursor.execute("PRAGMA table_info(water_saving_entry)")
    columns = [row[1] for row in cursor.fetchall()]
    
    needed_columns = [
        ('bill_images', 'TEXT DEFAULT "[]"'),
        ('suggestions', 'TEXT DEFAULT "[]"'),
        ('school_logo', 'TEXT DEFAULT ""'),
        ('student_avatar', 'TEXT DEFAULT ""'),
        ('teacher_name', 'TEXT DEFAULT ""') # Ensure this exists
    ]
    
    for col_name, col_type in needed_columns:
        if col_name not in columns:
            print(f"Adding column {col_name}...")
            cursor.execute(f"ALTER TABLE water_saving_entry ADD COLUMN {col_name} {col_type}")
            
    conn.commit()
    conn.close()
    print("Migration completed.")

if __name__ == "__main__":
    migrate()
