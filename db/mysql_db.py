import mysql.connector
from config import MYSQL_CONFIG

def get_mysql_connection():
    """
    Returns a MySQL connection and cursor
    """
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    return conn, cursor
