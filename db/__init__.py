# Import database connection functions
from .mysql_db import get_mysql_connection
# from .mongo_db import get_mongo_collection

# -------------------------------
# Initialize connections
# -------------------------------

# MySQL connection
mysql_conn, mysql_cursor = get_mysql_connection()

# # MongoDB collection
# mongo_collection = get_mongo_collection()
