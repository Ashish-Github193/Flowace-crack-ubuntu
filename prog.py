import os
import shutil

import sqlite3

from conf import IN_USE_FILE, LOCAL_FILE


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


def remove_db_file(file_path) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def main() -> None:
    copy_database(IN_USE_FILE, LOCAL_FILE)
    conn, cursor = connect_to_database(LOCAL_FILE)

    print("=" * 50)
    active_windows = select_active_windows(cursor)
    print(*active_windows, sep="\n")

    conn.close()


if __name__ == "__main__":
    main()
