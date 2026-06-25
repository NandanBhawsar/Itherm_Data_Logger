import csv
import sqlite3

def export_logs():

    db = sqlite3.connect(
        "app.db"
    )

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM logs"
    )

    rows = cursor.fetchall()

    with open(
        "logs.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(
            file
        )

        writer.writerow(
            [
                "Timestamp",
                "PV",
                "SP",
                "OUTPUT"
            ]
        )

        writer.writerows(
            rows
        )