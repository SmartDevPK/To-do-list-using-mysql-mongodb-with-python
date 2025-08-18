import mysql.connector
from config import MYSQL_CONFIG

mysql_conn = mysql.connector.connect(MYSQL_CONFIG)
mysql_cursor = mysql_conn.cursor()

