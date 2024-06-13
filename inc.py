import os
import shutil
from datetime import datetime

import sqlite3

from conf import IN_USE_FILE, LOCAL_FILE
from utils import get_columns_and_placeholders, get_timzone_substracted


def copy_database(source, destination) -> None:
    if os.path.exists(destination):
        os.remove(destination)
    shutil.copy(source, destination)


def connect_to_database(database_file) -> tuple:
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    return conn, cursor


def select_active_windows(cursor) -> list:
    cursor.execute("SELECT * FROM active_windows")
    return cursor.fetchall()


def update_active_window(cursor, entry_id) -> None:
    if entry_id is None:
        print("No active windows found")
        return

    cursor.execute(
        f"""
            UPDATE active_windows
            SET duration = 360000,
                appName = 'Google-chrome'
            WHERE id = ?
            """,
        (entry_id,),
    )


def delete_all_entries(cursor) -> None:
    cursor.execute("DELETE FROM active_windows")


def insert_new_entry(cursor, columns: list, placeholders: list) -> None:
    cursor.execute(
        f"""
            INSERT INTO active_windows
            ({', '.join(columns)})
            VALUES
            ({', '.join(['?' for _ in range(len(columns))])})
            """,
        placeholders,
    )


def commit_and_close_connection(conn) -> None:
    conn.commit()
    conn.close()


def main(start_datetime: datetime, end_datetime: datetime) -> None:
    copy_database(IN_USE_FILE, LOCAL_FILE)
    conn, cursor = connect_to_database(LOCAL_FILE)

    print("=" * 50)
    active_windows = select_active_windows(cursor)
    print(*active_windows, sep="\n")

    first_entry_id = active_windows[0][0] if active_windows else None
    if not first_entry_id:
        raise ValueError("No active windows found")

    delete_all_entries(cursor)

    for columns, placeholders in get_columns_and_placeholders(
        start_id=first_entry_id,
        start_date=start_datetime,
        end_date=end_datetime,
    ):
        insert_new_entry(cursor, columns, placeholders)

    commit_and_close_connection(conn)

    shutil.copy(LOCAL_FILE, IN_USE_FILE)


if __name__ == "__main__":
    start_dt = datetime(2024, 6, 13, 9, 30, 0)
    end_dt = datetime(2024, 6, 13, 19, 45, 0)

    main(
        start_datetime=get_timzone_substracted(dt=start_dt),
        end_datetime=get_timzone_substracted(dt=end_dt),
    )
