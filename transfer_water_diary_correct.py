import sqlite3
import os

dev_db_path = r"c:\Users\enesb\Desktop\projects\school-projects-platform\instance\projects.db"
prod_db_path = r"c:\Users\enesb\Desktop\projects\projects.db"

conn_dev = sqlite3.connect(dev_db_path)
cursor_dev = conn_dev.cursor()

# Get all water_saving_entry from DEV
cursor_dev.execute("SELECT student_name, school, volume_saved, created_at, city FROM water_saving_entry")
dev_entries = cursor_dev.fetchall()
conn_dev.close()

conn_prod = sqlite3.connect(prod_db_path)
cursor_prod = conn_prod.cursor()

# Get existing to prevent duplicates
cursor_prod.execute("SELECT student_name, total_consumption FROM water_saving_entry")
prod_existing = set(cursor_prod.fetchall())

insert_sql = """
INSERT INTO water_saving_entry (
    student_name, school_name, total_consumption, created_at, 
    teacher_name, family_size, month_data, bill_images, suggestions, school_logo, student_avatar
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

inserted_count = 0
for row in dev_entries:
    student_name, school, volume_saved, created_at, city = row
    
    # Check duplicate
    if (student_name, volume_saved) in prod_existing:
        continue
        
    # Map fields
    school_name = school if school else ""
    if city and city.lower() not in school_name.lower():
        school_name = f"{school_name} - {city}".strip(" -")
        
    total_consumption = volume_saved if volume_saved else 0.0
    
    # Defaults for other fields
    teacher_name = ""
    family_size = 4
    month_data = "[]"
    bill_images = "[]"
    suggestions = "[]"
    school_logo = ""
    student_avatar = ""
    
    values = (
        student_name, school_name, total_consumption, created_at,
        teacher_name, family_size, month_data, bill_images, suggestions, school_logo, student_avatar
    )
    
    try:
        cursor_prod.execute(insert_sql, values)
        inserted_count += 1
        prod_existing.add((student_name, total_consumption))
    except Exception as e:
        print(f"Error inserting {student_name}: {e}")

conn_prod.commit()
print(f"Successfully migrated {inserted_count} old records into PROD DB.")
conn_prod.close()
