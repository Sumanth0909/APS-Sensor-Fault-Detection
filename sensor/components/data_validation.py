# we will create a component (within training pipeline) for data validation
# this file is inline with "data_ingestion.py" file inside the "components" folder

from sensor.entity import artifact_entity
from sensor.entity import config_entity
from sensor.logger import logging
from sensor.exception import SensorException
import os   
import sys
import pandas as pd
import numpy as np
from typing import Optional
from sensor.utils import utils
from sensor.config import TARGET_COLUMN

from scipy.stats import ks_2samp

class DataValidation:
    # "data_validation_config" is the input to the "Data Validation" component            
    # "data_validation_config" is of type- (file name. data type) 'config_entity.DataValidationConfig'
    # also, the output of "data ingestion" phase -- ie "data_ingestion_artifact" -- is the input to "data validation" phase
    # "data_ingestion_artifact" is of the type "artifact_entity.DataIngestionArtifact"
    def __init__(self, data_validation_config:config_entity.DataValidationConfig, data_ingestion_artifact:artifact_entity.DataIngestionArtifact):

        try: 
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}") 
            self.data_validation_config = data_validation_config

            self.data_ingestion_artifact = data_ingestion_artifact

            # this dictionary contains all the errors related to validation
            # we will use this to prepare the validation error report
            self.validation_error = dict() 
        
        except Exception as e:
            raise SensorException(e, sys)    

    # this function will -- drop the columns if there are many missing values
    # (ie if there are many missing values above some threshold 
    # this threshold is taken from "config_entiy.py" file inside the "entity" folder
    # "df" is of the type of pandas.dataframe
    # and this function returns another pandas.dataframe
    # 'Option[pd.DataFrame]' => we used "Option" as - if all the columns have 30% of its values 
    #         as null values, then each and every column will be dropped and we may get a empty dataframe
    # "report_key_name" is required to log the information inside the "reports" properly 
    # and SEPARATELY for "train file" and "test file" 
    # because a "key" inside a dictionary, can have only one/unique value -- it cannot be changed/modified
    # when "test file" comes up (assuming that 1st we take "train file" and then "test file")
    # so, this "report_key_name:str" will be used in each and every function inside the
    # class "DataValidation"
    # or in other words, just to have things separate-separate 
    # for better understanding, refer the usage of "report_key_name:str" in 
    # the function "initiate_data_validation"
    def drop_missing_values_columns(self, df:pd.DataFrame, report_key_name:str) -> Optional[pd.DataFrame]:
        try:
            logging.info("selecting column names which has NULL values above {threshold}")
            # this threshold is taken from "config_entiy.py" file inside the "entity" folder
            # in that, "data_validation_config" function -- and in that "missing_threshold" variable
            threshold = self.data_validation_config.missing_threshold
            drop_column_names = []    # a list which contains the names of columns which we will drop
                          # ie those columns whose null values are > 30% of total number of values in that column

            for column_name, missing_percentage in zip((df.isnull().sum()/df.shape[0]).index,(df.isnull().sum()/df.shape[0]).values):
                print(column_name, missing_percentage * 100)
                if missing_percentage > threshold:
                    drop_column_names.append(column_name)  
            
            # we will update all the dropped columns in the "validation_error" dictionary
            logging.info("columns to be dropped: list({drop_column_names})")
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names), axis=1, inplace=True)  

            if len(df.columns) == 0:    # ie if all the columns are droppped, return a None
                return None
            return df                              

        except Exception as e:
            raise SensorException(e,sys)

    # we want to validate -- whether the required columns exists
    # to do this, we have to pass these 2 dataframes -- base dataframe and current dataframe
    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:# gives "boolean" output (ie True or False)
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

# this is a list which contains those columns which are present in the base dataframe, but is missing in the current dataframe
            missing_columns = []  
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info("column {base_column} is not available")
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name] = missing_columns
                return False
            
            return True 

        except Exception as e:
            raise SensorException(e,sys)

    # data drift = a phenomenon that occurs when the statistical properties of data used to train a
            # machine learning model change over time. This can cause a model's performance to degrade.
    # or when the statistical properties of old/base data and that of new data -- is different
    # this function will be used to detect 'data drift' and to then prepare the data drift report 
    # this will not return anything -- we will just prepare the data drift report        
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame, report_key_name:str):
        try:
            # we will use this dictionary to prepare the data drift report
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                same_distribution = ks_2samp(base_data, current_data) # this gives p-value

# we reject null hypothesis -- if "p-value" < 0.05   (ie we accept the alternate hypothesis)
# ie if "p-value" <= 0.05   => both have different distribution, ie there is a data drift 
#                             and so, we have to RE-TRAIN our model 
# ie if "p-value" > 0.05  =>  both have same distribution
                if same_distribution.pvalue > 0.05 :
                    # both have same distribution and so, there is no data drift
                    drift_report[base_column] = {
                        "p values" : float(same_distribution.pvalue),
                        "is_same_distribution?" : True
                    }

                else:
                    # both have different distribution and so, there is a data drift
                    drift_report[base_column] = {
                        "p values" : float(same_distribution.pvalue),
                        "is_same_distribution?" : False
                    }

            self.validation_error[report_key_name] = drift_report

        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
    # ie the output of this function is- (file name. data type) 'artifact_entity.DataIngestionArtifact'
        try:
            logging.info(f"reading base dataframe")
            # first, we have to read the base/old file (or dataframe)
            base_df = pd.read_csv(self.data_validation_config.base_file_path)

            logging.info(f"replacing na values to np.NAN in base dataframe")
            # base/old file (or dataframe) has "na" -- so, we will replace it with "np.NAN"
            base_df.replace("na",np.NAN, inplace=True)

            logging.info(f"dropping NULL values columns from base dataframe")
            # we will drop the columns which have null values > threshold
            # so, we will call the function "drop_missing_values_columns"
            base_df = self.drop_missing_values_columns(df = base_df, report_key_name= "missing_values_within_base_dataset")
            # CAREFULLY REFER THE USAGE OF "report_key_name:str" above
            # WE WILL USE "report_key_name:str" IN A SIMILAR WAY, EVERYWHERE ELSE

            # now, we will read the "train file" and "test file"
            # the output of "data ingestion" phase -- ie "data_ingestion_artifact" -- is the input to "data validation" phase
            logging.info(f"reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path) 
            logging.info(f"reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # we will drop the columns which have null values > threshold -- from both "train file" and "test file"
            # so, we will call the function "drop_missing_values_columns"
            logging.info(f"dropping NULL values columns from train dataframe")
            train_df = self.drop_missing_values_columns(df = train_df, report_key_name= "missing_values_within_train_dataset")
            logging.info(f"dropping NULL values columns from test dataframe")
            test_df = self.drop_missing_values_columns(df = test_df, report_key_name= "missing_values_within_test_dataset")

            # refer "utils.py" file inside the "utils" folder -- (C) --
            # since the target column SHOULD BE a string itself, and is not to be converted to float,
            # we will create this variable called as "exclude_columns" which is a list
            # this will be used inside the "utils.py" file inside the "utils" folder -- (C) --
            # "exclude_columns" will again return back the modified "base_df"
            # refer the "utils.py" file inside the "utils" folder -- (C) -- 
            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns= exclude_columns)

            # similarly, we will use it for "train_df" and "test_df"
            train_df = utils.convert_columns_float(df=train_df, exclude_columns= exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns= exclude_columns)


            # now, we will check whether the required columns exists or not -- inside from both "train file" and "test file"
            logging.info(f"do we have all the required columns in train dataframe?")
            train_df_columns_status = self.is_required_columns_exists(base_df= base_df, current_df= train_df, report_key_name= "missing_columns_within_train_dataset")
            logging.info(f"do we have all the required columns in test dataframe?")
            test_df_columns_status = self.is_required_columns_exists(base_df= base_df, current_df= test_df, report_key_name= "missing_columns_within_test_dataset")

            # only if "train_df_columns_status" is "True", only then we can go for "data drift" detection 
            # ie whether there is "data drift" or not
            # we will do it for both "train file" and "test file"

            if train_df_columns_status:   # ie if train_df_columns_status == True
                logging.info(f"as all the columns are available in train dataframe, hence detecting data drift")
                self.data_drift(base_df= base_df, current_df= train_df, report_key_name= "data_drift_within_train_dataset")

            if test_df_columns_status:    # ie if test_df_columns_status == True
                logging.info(f"as all the columns are available in test dataframe, hence detecting data drift")
                self.data_drift(base_df= base_df, current_df= test_df, report_key_name= "data_drift_within_test_dataset") 

            # we have to write/prepare the report -- in ".yaml"
            logging.info(f"write the report in yaml file")
            utils.write_yaml_file(file_path= self.data_validation_config.report_file_path, data= self.validation_error)
            
            # now, everything is done -- so we get the output of 
            # "Data Validation" phase ie "data_validation_artifact"
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path= self.data_validation_config.report_file_path)
            logging.info("data validation artifact : {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e,sys)

