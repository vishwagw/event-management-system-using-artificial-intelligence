# libs:
import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, '..', 'data', './Config/DB_files/sample_event.db')

# function for geeting the connection for the system model
def get_connection():
    return sqlite3.connect(DB_PATH)

# to get the table of atendees:
def drop_table():
    connect = get_connection()
    con = connect.cursor()
    con.execute('DROP TABLE attendees')
    connect.commit()
    print("Table dropped successfully")
    connect.close()

# intiliaze the DBfile for event
def initialize_DB():
    connect = get_connection()
    con = connect.cursor()
    con.execute(
        # TODO: create a data table for atendees
    )

    connect.commit()
    connect.close()


