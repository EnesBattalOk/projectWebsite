import sqlite3
import os

dev_db_path = r"c:\Users\enesb\Desktop\projects\school-projects-platform\instance\projects.db"
prod_db_path = r"c:\Users\enesb\Desktop\projects\projects.db"

# Connect to DEV db
print(f"Connecting to DEV DB: {dev_db_path}")
conn_dev = sqlite3.connect(dev_db_path)
cursor_dev = conn_dev.cursor()

# Get all water_saving_entry records from DEV db
cursor_dev.execute("SELECT * FROM water_saving_entry")
dev_entries = cursor_dev.fetchall()

# Get column names
column_names = [description[0] for description in cursor_dev.description]
print(f"Found {len(dev_entries)} entries in DEV DB.")

conn_dev.close()

# Connect to PROD db
print(f"Connecting to PROD DB: {prod_db_path}")
conn_prod = sqlite3.connect(prod_db_path)
cursor_prod = conn_prod.cursor()

# Check what's in PROD DB currently
cursor_prod.execute("SELECT COUNT(*) FROM water_saving_entry")
prod_count = cursor_prod.fetchone()[0]
print(f"PROD DB currently has {prod_count} entries.")

# To prevent duplicate id constraints if they conflict, let's just insert them without the existing ID so sqlite generates new ones
# Actually, since it's just a simple table, let's see its schema
cursor_prod.execute("PRAGMA table_info(water_saving_entry)")
schema = cursor_prod.fetchall()
print("PROD Schema:", schema)

# Prepare insert statement. Let's assume ID is column 0 and autoincrements, so we omit it to avoid conflicts.
cols_no_id = [col for col in column_names if col != 'id']
placeholders = ', '.join(['?'] * len(cols_no_id))
insert_sql = f"INSERT INTO water_saving_entry ({', '.join(cols_no_id)}) VALUES ({placeholders})"

# Find indices of cols_no_id
col_indices = [column_names.index(col) for col in cols_no_id]

# In DEV db, find duplicate names and quantities inside PROD db so we don't insert totally identical
cursor_prod.execute("SELECT student_name, volume_saved FROM water_saving_entry")
prod_existing = set(cursor_prod.fetchall())

inserted_count = 0
for entry in dev_entries:
    # Get values for no_id columns
    values = [entry[i] for i in col_indices]
    
    # check if (student_name, volume_saved) already in PROD
    name_idx = cols_no_id.index("student_name")
    vol_idx = cols_no_id.index("volume_saved")
    
    if (values[name_idx], values[vol_idx]) not in prod_existing:
        cursor_prod.execute(insert_sql, values)
        inserted_count += 1
        prod_existing.add((values[name_idx], values[vol_idx]))

conn_prod.commit()
print(f"Successfully inserted {inserted_count} missing entries into PROD DB.")
conn_prod.close()
