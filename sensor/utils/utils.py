#-------------------------------------------------------------------------------------------------
# (A)
import pandas as pd
from sensor.config import mongo_client
import os
import sys
import yaml
import dill
import numpy as np

from sensor.logger import logging              # These 2 are v.v.imp
from sensor.exception import SensorException   # We will import them and use them in every file

# get_collection_as_dataframe() -> pd.DataFrame: -- means that this function gives the output as
# a pandas dataframe
# we have to give these two inputs to the function --
# database_name which is a string   and   collection_name which is a string 
# database_name and collection_name -- are to be taken from MongoDB
def get_collection_as_dataframe(database_name:str, collection_name:str) -> pd.DataFrame:
    try:       # (B)
        logging.info("reading Data from DataBase: {database_name} and Collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find())) 
        return df
    
    except Exception as e:
        raise SensorException(e, sys)    

    # mongo_client[database_name][collection_name].find() -- just generates all the data in one go
    # but we want in the form of a list, 
    # so list(mongo_client[database_name][collection_name].find())
    # pd.DataFrame(list(mongo_client[database_name][collection_name].find())) -- gives DataFrame
      
    # ".find()" -- finds all the documents from the "documents" (inside MongoDB)
    # in our case, it is around 36k documents from MongoDB 
    # where each document = one row/one record from our original csv file

    # we will also use our exceptions and logger module
      


#-------------------------------------------------------------------------------------------------
#  (B)    

def write_yaml_file(file_path, data:dict):
    try:
        # we will create directory
        file_dir = os.path.dirname(file_path)

        # now that we got file directory, next we will create the directory/folder
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "w") as file_writer:   # we will open the file in "write" mode
            # we will "write"/"dump" all the "data" that we have got using "file_writer"
            # ie using the "file_writer", all the data will be dumped/written in the (given) "file_path"
            yaml.dump(data, file_writer) 

    except Exception as e:
        raise SensorException(e,sys)
    
# ---------------------------------------------------------------------------------------------------
#  (C)

'''
After executing the file "data_validation.py" inside the "components" folder, we see that the 
output from "base dataframe" is a "string" and the output from "train dataframe and test dataframe" is 
a "float". So to do the data conversion, let us write a helper function
'''

# this function takes inputs as --  a dataframe and a list of columns which should be excluded
def convert_columns_float(df:pd.DataFrame, exclude_columns:list):
    try:

        for column in df.columns:
            if column not in exclude_columns:
                df[column] = df[column].astype('float')
        return df  
# ie, convert the column to float -- if that column does not belong to the list of "exlude_columns"            
        
    except Exception as e:
        raise SensorException(e,sys)      
    
#-------------------------------------------------------------------------------------------------
#  (D)

'''
We have to save our target encoder. 
It is better if we define some functions to save and load our objects as ".pkl" files. 
To do this, we will define some helper functions.
'''

# we need to give the location where we want to save, and the object which we want to save -- as inputs
# we have imported "dill" -- ie import dill
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("exited the save_object method of utils")
    except Exception as e:
        raise SensorException(e, sys) from e


# we need to give the location where we want to save, and the object which we want to save -- as inputs
# we have imported "dill" -- ie import dill
# first, we will check whether the files exists in the given path or not - if yes, we will load it
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"the file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e
    
# ---------------------------------------------------------------------------------------------------
#  (E)

'''
When we are transforming our datasets, our dataframes are getting converted to arrays.
So, we need to have a function which can save our numpy array as a file and
also one more function to load that file into an numpy array format ie the file that we have saved, it 
should be loaded back as a numpy array. To do this, we will define some helper functions.  
'''    

# we need to give the location where we want to save, and the array which we want to save -- as inputs
# and then, we will save that array into a file
def save_numpy_array_data(file_path: str, array: np.array):

    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise SensorException(e, sys) from e


# we need to give the location where we want to save -- as input
# and then, we will load that file into an numpy array format ie the file that we have saved, it 
# should be loaded back as a numpy array
def load_numpy_array_data(file_path: str) -> np.array:

    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """

    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
        
    except Exception as e:
        raise SensorException(e, sys) from e
    
