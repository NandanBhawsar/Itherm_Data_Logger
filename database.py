import sqlite3

db = sqlite3.connect("app.db")

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs(
    timestamp TEXT,
    pv REAL,
    sp REAL,
    output REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS alarms(
    timestamp TEXT,
    message TEXT
)
""")

db.commit()
db.close()

print("Database Ready")