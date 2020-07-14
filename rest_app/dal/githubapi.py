import sqlite3
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler


def githubrepoapi():
    print("This is github repo api function ")
    JobId = 1
    JobType = 'Github'
    CreatedAt = datetime.now()
    UpdatedAT = '15-07-20'
    JobObject = 'synchronize'

    sqlite_db = sqlite3.connect('Gitub.db')
    sqlite_db_cursor = sqlite_db.cursor()
    sqlite_db_cursor.execute("INSERT INTO repodetails VALUES(?,?,?,?,?)",(JobId, JobType, CreatedAt, UpdatedAT, JobObject))
    sqlite_db.commit()
    sqlite_db_cursor.close()
    sqlite_db.close()

if __name__ == '__main__':
    sqlite_db = sqlite3.connect('Gitub.db')
    sqlite_db_cursor = sqlite_db.cursor()

    sqlite_db_cursor.execute("""CREATE TABLE IF NOT EXISTS repodetails (
        JobId INTEGER,
        JobType TEXT,
        CreatedAt TEXT,
        UpdatedAT TEXT,
        JobObject TEXT
        )""")
    sqlite_db.commit()
    sqlite_db_cursor.close()
    sqlite_db.close()

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(githubrepoapi, 'interval', seconds=1)
while True:
            time.sleep(2)
