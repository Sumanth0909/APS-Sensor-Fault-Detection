# This py file is used to dump our csv file into MongoDB (in the form of 'json' files)
# Each row (from csv) is converted into a file (json file) inside MongoDB

import pymongo
import pandas as pd
import json


# Provide the mongodb localhost url to connect python to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017")


DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"
DATAFILE_PATH = r"E:\E\DATA SCIENCE INEURON\Machine Learning Projects (Industry Grade Projects)\1) Sensor Fault Detection\aps_failure_training_set1.csv"          


if __name__ == "__main__":
    df = pd.read_csv(DATAFILE_PATH)
    print(f"Rows and Columns: {df.shape}") # Just to see how many rows and columns are there in our data 

# Let us drop the indexes ie row indexes or row numbers
# and inplace = True -- means it is overwitten permanently in that df itself; no new df created               
    df.reset_index(drop = True, inplace=True)



# Now let us convert the dataframe into json files - so that we can dump these json files into mongodb


# we have to take "Transpose" of the df and then apply "to_json" inbuilt function
# and then we use "json.loads()" - so that any new object, is loaded as json file itself 
# and then we use ".values()" - so that we get all in the form of values only
# and then we will store this overall - as a list
# to use this "to_json()", we have imported "json" library in the beginnning 
    json_record = list(json.loads(df.T.to_json()).values())    
    print(json_record[9])    # Let us print one element of the list - Just to see how it looks
                         # This one record represents one row from csv file = one json file 

# Now that we have our json records, we have to now insert these json records inside mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

'''
Now that we have inserted the json_records inside our mongodb, we can now see a new folder 
named as "aps" -- inside it, we have a folder named "sensor" -- inside this,
we have 36k "Documents" -- ie each row/line in csv = is now converted into a separate
json document
'''      