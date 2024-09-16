# we will create a component (within training pipeline) for data transformation
# this file is inline with "data_ingestion.py" file inside the "components" folder

from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os
import sys
from sklearn.pipeline import Pipeline
import pandas as pd
from sensor import utils
import numpy as np
from sklearn.preprocessing import LabelEncoder
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sensor.config import TARGET_COLUMN
from dataclasses import dataclass

class DataTransformation: 
    
    # "data_transformation_config" is the input to the "Data Transformation" component            
    # "data_transformation_config" is of type- (file name. data type) 'config_entity.DataTransformationConfig'
    # we need the "train.csv" file and "test.csv" file --- so, we need to know where they are located
    # we have stored the location of "train.csv" file and "test.csv" file in the "DataIngestionArtifact"
    # so, we will pass "DataIngestionArtifact" as input to this function
    # "data_ingestion_artifact" is of type- (file name. data type) 'config_entity.DataIngestionArtifact'
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} data transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)

    @classmethod    
    # let us define the "transformer" object -- using which we will do the transformation
    # we are going to create the data transformation pipeline 
    # and so, we will import -- "from sklearn.pipeline import Pipeline"
    # this function will return a "Pipeline"
    def data_transformer_object(cls) -> Pipeline:  
        try:
            
            # in few of the rows in our dataset, we have NULL values 
            # so to impute(/fill) those values, we will use "SimpleImputer()"
            # strategy, we can experiment and see which works better
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)

            # In our dataset, most of the columns are numerical -- so we will use "RobustScaler()" 
            # it is useful whenever we have OUTLIERS in the data
            # (If we don't have outliers, we can use "standard scaler or minmax scaler")
            robust_scaler =  RobustScaler()
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
                ])
            return pipeline
        except Exception as e:
            raise SensorException(e,sys)  
        
    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:

            # we will read the train file and test file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            # we will now split the data into -- i) input features and ii) target column
            # (the target column name/output column is "class" -- which has 2 values -- "pos" or "neg")
            # i) let us select the input feature for train and test file
            input_features_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_features_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            # ii) let us select the target column for train and test file
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            # since our target column is CATEGORICAL ie "pos" or "neg", we have to convert it into
            # NUMERICAL -- so we will do labelling
            # we will use "LabelEncoder()"
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            # transformation on target columns of both "train.csv" and "test.csv"
            # LabelEncoder() -- outputs an array -- so "_arr"
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            # we have to now trasform the input features -- ie we have to apply
            # all the above transformations that we discussed so far, onto the input features
            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_features_train_df)

            # transforming input features
            # outputs an array -- so "_arr"
            input_feature_train_arr = transformation_pipleine.transform(input_features_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_features_test_df)



            # In our dataset we see that there is a lot of imbalance - "pos" is very less than "neg" 
            # in the target column. So to balance this, based on the dataset we will populate (/create) 
            # new datapoints for the "pos" class

            # we will use -- "SMOTETomek"
            # that is why we imported -- from imblearn.combine import SMOTETomek
            smt = SMOTETomek(random_state=42)
            logging.info(f"before resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")

            # we have to pass (x & y) ie x = input_feature_train_arr and y = target_feature_train_arr
            # we will override -- this is for train file
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"after resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            
            logging.info(f"before resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            # we have to pass (x & y) ie x = input_feature_train_arr and y = target_feature_train_arr
            # we will override -- this is for train file
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"after resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")


            # we have to save our target encoder. To do this, we will define some helper functions
            # It is better if we define some functions to save and load our objects as ".pkl" files. 
            # we have written the functions inside the file "utils.py" inside the "utils" folder

            # and also, When we are transforming our datasets, our dataframes are getting converted to arrays.
            # so, we need to have a function which can save our numpy array as a file 
            # and also one more function to load that file into an numpy array format 
            # ie the file that we have saved, it should be loaded back as a numpy array 
            # to do this, we will define some helper functions. 
            # we have written the functions inside the file "utils.py" inside the "utils" folder

            # now, the "input feature" and "target feature" -- are separated -- both in train file and test file
            # so, we have to now combine it together -- so, we will concatenate them
            # because we have to save it into one single file -- ie one single file for train and one single file for test
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            
            # now let us save all these -- one by one

            # i) let us the save the numpy arrays -- ie  train array and test array
            # it will automatically create the directory
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,
                                        array=test_arr)


            # ii) let us the save the transformation object, which is a pipeline object
            # ie transformation_pipeine
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
             obj=transformation_pipleine)

            # iii) let us the save the target encoder object ie label_encoder
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
            obj=label_encoder)


            # we have to prepare the data transformation artifact
            # all the above things which we saved, these are the data transformation objects
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path

            )

            logging.info(f"data transformation objects {data_transformation_artifact}")
            return data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e, sys)







        except Exception as e:
            raise SensorException(e,sys)        