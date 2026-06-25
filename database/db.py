import sqlite3

def get_db():

    return sqlite3.connect(
        "app.db"
    )


def init_db():

    db = get_db()

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