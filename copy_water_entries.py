import sqlite3
import os

dev_db_path = r"c:\Users\enesb\Desktop\projects\school-projects-platform\instance\projects.db"
prod_db_path = r"c:\Users\enesb\Desktop\projects\projects.db"

# We will attach dev to prod and copy table
conn = sqlite3.connect(prod_db_path)
conn.execute(f"ATTACH DATABASE '{dev_db_path}' AS devdb")
conn.execute("INSERT INTO main.water_saving_entry SELECT * FROM devdb.water_saving_entry")
conn.commit()
conn.close()

print("Successfully copied water_saving_entry records from DEV to PROD.")
