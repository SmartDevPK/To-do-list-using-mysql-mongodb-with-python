from db.mongo_db import get_mongo_connection
import config

#initialize mongodb using the config file
mongo_client  = get_mongo_connection(config.MONGO_URI)
db = mongo_client[config.MONGO_DB_NAME]

#User collection
user = db['users']

#Task collection
def create_task(title: str, description:str, status:str="pendinf"):
  """ Insert a new task with title, description status and date"""
  task = {
        title: title,
        description: description,
        status: status
    }
  
  result = user.insert_one(task)
  return str(result.inserted_id)

#Function to get all tasks
def get_all_tasks():
    """ Retrieve all tasks from the collection"""
    return list(user.find())