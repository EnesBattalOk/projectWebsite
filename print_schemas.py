import sqlite3
import os

dev_db_path = r"c:\Users\enesb\Desktop\projects\school-projects-platform\instance\projects.db"
prod_db_path = r"c:\Users\enesb\Desktop\projects\projects.db"

conn_dev = sqlite3.connect(dev_db_path)
print("DEV DB schema:")
print([col[1] for col in conn_dev.cursor().execute('PRAGMA table_info(water_saving_entry)').fetchall()])
conn_dev.close()

conn_prod = sqlite3.connect(prod_db_path)
print("PROD DB schema:")
print([col[1] for col in conn_prod.cursor().execute('PRAGMA table_info(water_saving_entry)').fetchall()])
conn_prod.close()
