import sqlite3
import os

dev_db_path = r"c:\Users\enesb\Desktop\projects\school-projects-platform\instance\projects.db"
prod_db_path = r"c:\Users\enesb\Desktop\projects\projects.db"

with open("schemas.txt", "w") as f:
    try:
        conn_dev = sqlite3.connect(dev_db_path)
        f.write("DEV DB schema:\n")
        f.write(",".join([col[1] for col in conn_dev.cursor().execute('PRAGMA table_info(water_saving_entry)').fetchall()]) + "\n")
        conn_dev.close()
    except Exception as e:
        f.write("DEV error: " + str(e) + "\n")

    try:
        conn_prod = sqlite3.connect(prod_db_path)
        f.write("PROD DB schema:\n")
        f.write(",".join([col[1] for col in conn_prod.cursor().execute('PRAGMA table_info(water_saving_entry)').fetchall()]) + "\n")
        conn_prod.close()
    except Exception as e:
        f.write("PROD error: " + str(e) + "\n")

