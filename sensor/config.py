'''
 Inside the "data_dump.py" file (inside the main folder ie "Sensor Fault Detection" folder),
 we had already created the connection to mongoDB. But there can be so many connections to our 
 project - which can cause confusion. So, the best practice is to -- create a new folder and maintain 
 the configurations (connections) there itself. So, let us create a new file.

 So, in this file we will  write connections related code -- for example, connection with MongoDB

'''

# Provide the mongodb localhost url to connect python to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017")

# However, it is not a good practice to hardcode the URL in the source code -- so we will create a 
# new file called as ".env" inside the main folder (ie inside the "Sensor Fault Detection" folder)
# this ".env" file is an "environment file" -- and we can read the values from it, anywhere else too

# Create a class called as "EnvironmentVariable" -- to read/access all the "environment variables"
import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os

# we will use "dataclasses" library 
# we are defining a "mongodb" variable -- it is a URL, which is a type of string whose value is
# given as "os.getenv("mongodb_url")" -- in which we will read the URL (from the ".env" file)
@dataclass
class EnvironmentVariable :
    mongo_db_url:str = os.getenv("MONGO_DB_URL")


env_var = EnvironmentVariable()  # we created an object/variable of the "EnvironmentVariable" class

mongo_client = pymongo.MongoClient(env_var.mongo_db_url)  
# we did all this so that -- next time if we want to call/use the "mongo_client" variable to make
# connections, we need not write the entire code again and again
# ie everytime you run the project, the connections can be done easily


TARGET_COLUMN = "class"

TARGET_COLUMN_MAPPING ={
    "pos" : 1,
    "neg" : 0
}

