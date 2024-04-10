"""
This module contains the installation script for the server configuration application.
"""
import sqlite3
import os
from sqlite3 import Error
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    """ create a database connection to a SQLite database """
    try:
        db_path = os.getenv('DB_PATH', 'database.db')
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)

    return None

def fetch_all_server_data_as_dicts(conn):
    """
    Query all rows in the server_data table and return them as a list of dictionaries
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM server_data")

    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]

    servers = []
    for row in rows:
        server = dict(zip(columns, row))
        servers.append(server)

    return servers

def upsert_server_data(conn, server_data):
    """
    Insert or update form data into the server_data table.
    The server_data should include nine elements:
    (id, name, auth_type, host, port, user, password, compress, allow_no_password).
    If id is None, a new record is created.
    """
    if len(server_data) != 9:
        raise ValueError("server_data must contain nine elements.")

    sql = '''
    INSERT INTO server_data(id, name, auth_type, host, port, user, password, compress, allow_no_password)
    VALUES(?,?,?,?,?,?,?,?,?)
    ON CONFLICT(id) DO UPDATE SET
    name=excluded.name,
    auth_type=excluded.auth_type,
    host=excluded.host,
    port=excluded.port,
    user=excluded.user,
    password=excluded.password,
    compress=excluded.compress,
    allow_no_password=excluded.allow_no_password
    '''
    cur = conn.cursor()
    cur.execute(sql, server_data)
    conn.commit()
    return cur.lastrowid

def delete_server_data(conn, server_id):
    """
    Delete a record from the server_data table by its id.

    :param conn: Connection object to the SQLite database
    :param id: ID of the record to delete
    """
    sql = 'DELETE FROM server_data WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (server_id,))
    conn.commit()
    if cur.rowcount > 0:
        print(f"Record with id {server_id} was deleted.")
    else:
        print(f"No record found with id {server_id}.")
