"""
This module contains the installation script for the server configuration application.
"""

from sqlite3 import Error
from enum import Enum
from dbs import create_connection

def create_table(connection, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

class Config(Enum):
    """Enum class representing configuration options."""
    CONFIG = 'config'
    PASSWORD = 'password'

SQL_CREATE_PROJECT_TABLE = " CREATE TABLE IF NOT EXISTS server_data (\
                                id integer PRIMARY KEY,\
                                name text NOT NULL,\
                                auth_type text,\
                                host text,\
                                port text,\
                                user text,\
                                password text,\
                                compress boolean,\
                                allow_no_password boolean\
                            ); "

# Create a database connection and table
CONN = create_connection()
if CONN is not None:
    create_table(CONN, SQL_CREATE_PROJECT_TABLE)
else:
    print("Error! cannot create the database connection.")
