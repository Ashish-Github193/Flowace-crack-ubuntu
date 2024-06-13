import os
import shutil

import sqlite3

from conf import *


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


def delete_entries(cursor) -> None:
    cursor.execute("DELETE FROM active_windows")


def commit_and_close_connection(conn) -> None:
    conn.commit()
    conn.close()


def main() -> None:
    copy_database(IN_USE_FILE, LOCAL_FILE)
    conn, cursor = connect_to_database(LOCAL_FILE)

    print("=" * 50)
    active_windows = select_active_windows(cursor)
    print(*active_windows, sep="\n")

    delete_entries(cursor)
    commit_and_close_connection(conn)

    shutil.copy(LOCAL_FILE, IN_USE_FILE)


if __name__ == "__main__":
    main()
