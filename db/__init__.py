from .mysql_db  import get_mysql_connection
from .mongo_db import get_mongo_collection

mysql_conn = get_mysql_connection
mongo_collection  = get_mongo_collection