import logging
import sqlite3


class SubmissionDB:
    def __init__(self, db_name) -> None:
        self._connection: sqlite3.Connection = sqlite3.connect(db_name)
        logging.info(f"Connection to DB '{db_name}' established")
        self._cursor: sqlite3.Cursor = self._connection.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS submissions (id TEXT PRIMARY KEY)")
        self._connection.commit()

    def submission_present(self, submission_id: str) -> bool:
        self._cursor.execute(f"SELECT * FROM submissions WHERE id = '{submission_id}'")
        submission_present: bool = self._cursor.fetchone()
        if submission_present: logging.info(f"Submission '{submission_id}' present in DB'")
        return submission_present
    
    def insert_submission(self, submission_id: str) -> None:
        self._cursor.execute(f"INSERT INTO submissions VALUES ('{submission_id}')")
        self._connection.commit()
        logging.info(f"Submission '{submission_id}' inserted into DB")