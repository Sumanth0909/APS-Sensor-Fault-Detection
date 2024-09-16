'''
Suppose we already had one model in production (ie one model was already being used). 
These models (which are already being used), are saved inside a folder called as "saved_models" inside the "sensor" folder.
And in the previous phase, we have completed "Model Training". 
Now, we have to compare the performance of both -- the model which was already in production and the newly trained model.
Whose performance is better, we will keep that model only

The task of the file "predictor.py" is to -- access/read the LATEST MODEL from the "saved_models" inside the "sensor" folder 
and based on this accessed/read model, do the PREDICTIONS 
'''

'''
We have our "saved model" (ie "model.pkl"), whenever we want to deploy it, along with "model.pkl", 
we also need the other saved objects or files ie "transformer.pkl" file, "target_encoder.pkl" etc 
ie all the other files too are required -- for our model to be used in production.
So, we need to define some helper function -- so that we can have/maintain all these files together 
ie in a single location/directory 
'''

'''
We do all this so that whatever files are generated during the training process, we can get
their locations and then we can load those files during PREDICTION also -- ie in the PREDICTION PIPELINE also
'''

import os
from sensor.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME,MODEL_FILE_NAME,TARGET_ENCODER_OBJECT_FILE_NAME
from glob import glob
from typing import Optional
import sys

class ModelResolver:
    
    # we have to pass on the location of "saved_models" -- as input
    # using this class, we will get location of all these ".pkl" files
    # once we have the location, we can easily load these files later on whenever needed
    def __init__(self,model_registry:str = "saved_models",
                transformer_dir_name="transformer",
                target_encoder_dir_name = "target_encoder",
                model_dir_name = "model"):

        self.model_registry=model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.target_encoder_dir_name=target_encoder_dir_name
        self.model_dir_name=model_dir_name


    # using this, we will pick the LATEST FOLDER (ie model)
    def get_latest_dir_path(self)->Optional[str]:

        try:
            # first, we will get all the folders' or dirs' names
            # then we will convert this to a list -- to get it in terms of strings
            # then we will convert these strings to int using 'map' function
            # then we will select the 'max' in this -- to get the LATEST
            dir_names = os.listdir(self.model_registry)
            if len(dir_names)==0:
                return None
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e:
            raise e
           
    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"model is not available")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"transformer is not available")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"target encoder is not available")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e


    # now, we will define the location where we want to save these files also --- on-by-one for each file
    # ie where we want to save the new files
    # suppose the latest files are saved in "saved_models/1" -- where "1" is the folder name which contains latest files
    # then, we want the NEXT INT -- ie "saved_models/2" -- to save the new files in "2" folder

    # also, for the first time ie when there is no folder at all in "saved_models", then
    # it should create the first folder as "0" ie "saved_models/0"


    def get_latest_save_dir_path(self)->str:
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir==None:
                return os.path.join(self.model_registry,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry,f"{latest_dir_num+1}")
        except Exception as e:
            raise e

    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e

    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e    