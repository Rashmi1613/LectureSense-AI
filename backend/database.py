import sqlite3
from pathlib import Path

DB_PATH = Path("database/lectures.db")


def get_connection():

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DB_PATH)


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lectures(

            lecture_id INTEGER PRIMARY KEY AUTOINCREMENT,

            lecture_name TEXT NOT NULL,

            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files(

            file_id INTEGER PRIMARY KEY AUTOINCREMENT,

            lecture_id INTEGER NOT NULL,

            file_type TEXT NOT NULL,

            file_name TEXT NOT NULL,

            file_path TEXT NOT NULL,

            FOREIGN KEY (lecture_id)
            REFERENCES lectures(lecture_id)

        )
    """)
    
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS ocr_results(

    ocr_id INTEGER PRIMARY KEY AUTOINCREMENT,

    lecture_id INTEGER NOT NULL,

    file_id INTEGER NOT NULL,

    extracted_text TEXT NOT NULL,

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (lecture_id)
        REFERENCES lectures(lecture_id),

    FOREIGN KEY (file_id)
        REFERENCES files(file_id)

)
""")

    conn.commit()
    conn.close()


# -----------------------------------------------------
# Lecture Operations
# -----------------------------------------------------

def create_lecture(lecture_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO lectures(lecture_name)
        VALUES(?)
        """,
        (lecture_name,)
    )

    lecture_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return lecture_id


# -----------------------------------------------------
# File Operations
# -----------------------------------------------------

def add_file(

        lecture_id,

        file_type,

        file_name,

        file_path

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO files
        (
            lecture_id,
            file_type,
            file_name,
            file_path
        )

        VALUES
        (?, ?, ?, ?)
        """,

        (
            lecture_id,
            file_type,
            file_name,
            file_path
        )

    )

    conn.commit()

    conn.close()


# -----------------------------------------------------
# Get Lecture History
# -----------------------------------------------------

def get_all_lectures():

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM lectures

        ORDER BY upload_time DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# -----------------------------------------------------
# Get Files of a Lecture
# -----------------------------------------------------

def get_files(lecture_id):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM files

        WHERE lecture_id=?

        """,

        (lecture_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

# to save ocr results in the database

def save_ocr_result(
    lecture_id,
    file_id,
    extracted_text
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ocr_results
        (
            lecture_id,
            file_id,
            extracted_text
        )

        VALUES
        (?, ?, ?)
        """,

        (
            lecture_id,
            file_id,
            extracted_text
        )

    )

    conn.commit()

    conn.close()
def get_ocr_results(lecture_id):

    conn = get_connection()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *

        FROM ocr_results

        WHERE lecture_id = ?
        """,
        (lecture_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
