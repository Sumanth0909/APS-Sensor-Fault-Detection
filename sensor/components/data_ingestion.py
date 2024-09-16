# we will create a component (within training pipeline) for data ingestion

from sensor import utils
from sensor.entity import config_entity      # we want input to the data ingestion component 
from sensor.entity import artifact_entity    # and also, we want output of the data ingestion component    
from sensor.exception import SensorException
from sensor.logger import logging
import os
import sys  
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self, data_ingestion_config:config_entity.DataIngestionConfig):
    # "data_ingestion_config" is the input to the "Data Ingestion" component            
    # "data_ingestion_config" is of type- (file name. data type) 'config_entity.DataIngestionConfig'

        try:
            logging.info(f"{'>>'*20} data ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
    # ie the output of this function is- (file name. data type) 'artifact_entity.DataIngestionArtifact'

        try:
            logging.info(f"exporting collection data as pandas dataframe")
            # exporting collection data as pandas dataframe
            df:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)

            logging.info("replace na values with np.Nan")
            # replace na with np.Nan -- because we had some missing values in the data
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            logging.info("save data in feature store")
            # save data in feature store
            logging.info("create feature store folder if not available")
            # create feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info("save df to feature store folder")
            # save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)


            logging.info("split dataset into train set and test set")
            # split dataset into train and test set
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
            
            logging.info("create dataset directory folder if not available")
            # create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("save df to feature store folder")
            # save df to feature store folder
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            # prepare output/artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
    
        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)         