'''
For any ML Project, the TRAINING PIPELINE is as follows -
Data ingestion-> Data validation-> Data transformation-> Model trainer-> Model evaluation-> Model pusher
(There is nothing called as "Testing" pipeline)

For each of these components(blocks), we will create one class
'''
# Three dots (...) is equal to = "pass" keyword

import os
import sys
from sensor.exception import SensorException
from sensor.logger import logging
from datetime import datetime

FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

# also, there is one more input  -ie "TrainingPipelineConfig"
# we will start with the "TrainingPipelineConfig" class
# i want to store each and every outputs/files/graphs/figs/models/metrics etc - each and every outputs 
# in a single place -- example, we are getting each and every log inside the "logs" folder inside the
# main project folder ie "Sensor Fault Detection" folder
# so to do this, we will use the folder "artifacts" -- we will CREATE A NEW FOLDER called as "artifacts"

# ie each and everytime we run the "training pipeline", there should be a NEW FOLDER CREATED everytime
# called as "artifacts" along with time stamp
class TrainingPipelineConfig:
    def __init__(self):
        self.artifact_dir = os.path.join(os.getcwd(),"artifacts", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        # os.getcwd() -- gives the current directory -- and then in  the current directory, we
        # will CREATE A NEW FOLDER called as "artifacts"
        # with time stamp WITHIN this order -f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        # ie month day year__hour min sec    format
        # so overall, it will look something like this -- artifacts/(time stamp)
        # (time stamp) folder is inside "artifacts" folder

class DataIngestionConfig:

    # we will create an object called as "training_pipeline_config" 
    # which belongs to the "TrainingPipelineConfig" class and its type is "TrainingPipelineConfig"
    # we ourselves have defined this
    # we will pass this object to this class too
    # this object should be available to each and every component of the training pipeline
    # ie it should be available to each and every class
    # (Just like -- each and every component has access to the training pipeline)
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try: 
            # now, we have to generate the output for "Data Ingestion"
            self.database_name = "aps"
            self.collection_name = "sensor"

            # now, we want to creare a folder named as "data_ingestion"
            # and we want to merge this with the above ("artifacts"/ time stamp) folder
            # so that overall, it looks like this -- ("artifacts" / time stamp /"data_ingestion") folder
            # (time stamp) folder is inside "artifacts" folder and "dat_ingestion" folder is inside (time stamp) folder
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")

            # when we will download the dataframe from mongodb, we have to store the dataframe somewhere
            # so, we have to prepare the location where we want to store the dataframe 
            # "feature_store" is a common name given for this -- so, we will also use the same name
            # 'feature_store' is a place from where you can get the data for the training pipeline
            # ie for the training pipeline, the data is got from 'feature_store' and not directly from
            # the database (MongoDB)
            # the below code creates "sensor.csv" file inside "feature_store"
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)

            # ALSO, IN DATA INGESTION, WE WILL SPLIT THE DATA INTO "TRAIN FILE" AND "TEST FILE"
            # in below, "dataset" is a common folder which contains both "train.csv" and "test.csv"
            # the below code creates "train.csv" file and "test.csv" file inside "dataset" folder
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2

        except Exception as e:
            raise SensorException(e,sys)    

    # we want to get all the data from "train.csv" and "test.csv" , in the form of a dictionary 
    # => the output of this function is a dictionary 
    def to_dict(self,) -> dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e,sys)    

class DataValidationConfig:
    
    try:
        # refer the above class - "class DataIngestionConfig:"
        # all the classes below, will be on the same lines

        # training_pipeline_config:TrainingPipelineConfig - this object should 
        # be available to each and every component of the training pipeline
        def __init__(self, training_pipeline_config:TrainingPipelineConfig):
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")

            # we will create some 'validation reports'-that whether new data is inline with old data
            # the name of this report file is - "report.yaml" -- it can be ".yaml" file or ".json" file
            # we will create it within the "data_validation" folder
            self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")

            # let us drop those columns in which the number of missing values > 20% of total number of values in that column
            # normally, we use 20% itself -- so, let us use 20% here also
            self.missing_threshold:float = 0.2

            # we need the path where we have our base/old file (or dataframe)
            self.base_file_path = os.path.join("E:\E\DATA SCIENCE INEURON\Machine Learning Projects (Industry Grade Projects)\1) Sensor Fault Detection\aps_failure_training_set1.csv")

    except Exception as e:
        raise SensorException(e,sys)
    
class DataTransformationConfig:
    try:
        # training_pipeline_config:TrainingPipelineConfig - this object should 
        # be available to each and every component of the training pipeline
        def __init__(self, training_pipeline_config:TrainingPipelineConfig):
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_transformation")

            # we will define the "data transform object" -- we will save the path for this "data transform object"
            # we can use ".obj" or ".pkl" -- here we will use ".pkl"
            self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer" , TRANSFORMER_OBJECT_FILE_NAME)
            
            # we will store the transformed train and test files
            # ".replace("csv","npz")" -- so that we will get the files in ".npz" format ie np array format ; and not in ".csv" format
            self.transformed_train_path = os.path.join(self.data_transformation_dir, "transformed" , TRAIN_FILE_NAME.replace("csv","npz"))
            self.transformed_test_path = os.path.join(self.data_transformation_dir, "transformed" , TEST_FILE_NAME.replace("csv","npz"))

            # we will have to define the path to store the "target encoder"
            # we can use ".obj" or ".pkl" -- here we will use ".pkl"
            self.label_encoder_path = os.path.join(self.data_transformation_dir, "target encoder" , TARGET_ENCODER_OBJECT_FILE_NAME)
    
    except Exception as e:
        raise SensorException(e,sys)

class ModelTrainerConfig:
    try:
        # training_pipeline_config:TrainingPipelineConfig - this object should 
        # be available to each and every component of the training pipeline

        # we will save our model in the "model_path" path -- so, we need to 1st see "mode_trainer_dir"
        # we will create a folder named as "model_trainer" inside this path and save it there
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir , "model_trainer")
            self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)

            # expected score = we want our model to have score ATLEAST MORE THAN expected score
            # for example - 70% (ie 0.7)
            self.expected_score = 0.7

            # overfitting = if train score is good but test score is bad,
            # ie if train score > expected score   &    test score < expected score
            # we will take difference (train score - expected score) and if this difference 
            # is more than some "overfitting threshold", then we will tell that "our model is overfitting"
            # example - "overfitting threshold" = 10% (ie 0.1)
            self.overfitting_threshold = 0.1

    except Exception as e:
        raise SensorException(e,sys) 
           
class ModelEvaluationConfig:

    try:

        # training_pipeline_config:TrainingPipelineConfig - this object should 
        # be available to each and every component of the training pipeline
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            # "change threshold = 0.01" => if the (newly) trained model performs better by 1% 
            # as compared to the model which is already being used in production, then we
            # will accept the (newly) trained model
            self.change_threshold = 0.01

    except Exception as e:
        raise SensorException(e,sys)        

class ModelPusherConfig:

    try:

        # training_pipeline_config:TrainingPipelineConfig - this object should 
        # be available to each and every component of the training pipeline
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            # we will create a "model_pusher" directory/folder
            self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir , "model_pusher")

            # we will create a folder named as "saved_model" -- which is not inside/within any folder
            # it is an independent folder
            self.saved_model_dir = os.path.join("saved_models")

            # inside the "model_pusher" folder, we will create another "saved_models" folder
            # NOTE that this is the 2nd time we are creating "saved_models" folder
            # but location is different
            self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")

            # these 3 are the locations were we want to save the 3 objects
            # ie the files "transformer.pkl","model.pkl","target_encoder.pkl"
            self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
            self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
            self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_FILE_NAME)

    except Exception as e:
        raise SensorException (e,sys)
    