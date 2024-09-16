# we will create a component (within training pipeline) for model training
# this file is inline with "data_ingestion.py" file inside the "components" folder

from sensor.entity import artifact_entity,config_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
import os
import sys
from xgboost import XGBClassifier
from sensor import utils
from sklearn.metrics import f1_score

class ModelTrainer:

    # "model_trainer_config" is the input to the "Model Trainer" component            
    # "model_trainer_config" is of type- (file name. data type) 'config_entity.ModelTrainerConfig'
    # also, the output of "data transformation" phase -- ie "data_transformation_artifact" -- is the input to "model trainer" phase
    # "data_transformation_artifact" is of the type "artifact_entity.DataTransformationArtifact"
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} model trainer {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

    # refer the file "APS_failure_prediction.ipynb" inside the "EDA and Preprocessing" folder
    # there it is clearly proved that for our dataset, "XGBosst Classifier" is the best model   
    # we will use "XGBoost Classifier" model to do the training    
    def train_model(self,x,y):
        try:
            xgb_clf =  XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)   


    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            # let us load the numpy arrays ie train array and test array
            logging.info(f"loading train and test array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            # let us split input and target feature from both train and test array
            # we want each column except for the last column (because last column is the target feature)
            logging.info(f"splitting input and target feature from both train and test array")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            # let us train the model
            logging.info(f"train the model")
            model = self.train_model(x=x_train,y=y_train)

            # let us now do the prediction and calculate f1 score wrt train and test
            logging.info(f"calculating f1 train score")
            yhat_train = model.predict(x_train)
            f1_train_score  =f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score  =f1_score(y_true=y_test, y_pred=yhat_test)
            
            logging.info(f"train score:{f1_train_score} and test score {f1_test_score}")


            # let us check for overfitting or underfiiting or expected score
            # expected score = we want our model to have score ATLEAST MORE THAN expected score
                               # for example - 70% (ie 0.7)
                               # we have set this "expected_score" inside the "config_entity.py" 
                               # inside the "entity" folder

            # underfitting = if both train score and test score are bad, ie if both are less than
            #                excpected score
            logging.info(f"checking if our model is underfitting or not")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")

            # overfitting = if train score is good but test score is bad,
            #               ie if train score > expected score   &    test score < expected score
                            # we will take difference (train score - expected score)
                            # if this difference is more than some "overfitting threshold", 
                            # then we will tell that "our model is overfitting"
                            # example - "overfitting threshold" = 10% (ie 0.1)
                            # we have set this "expected_score" inside the "config_entity.py" 
                            # inside the "entity" folder
            logging.info(f"checking if our model is overfiiting or not")
            diff = abs(f1_train_score-f1_test_score)
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            # if everything is good, then there will be NO EXCEPTIONS RAISED
            # then we will ACCEPT the model
            # and then, we will save the trained model
            logging.info(f"saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # in the end, let us prepare artifact
            logging.info(f"prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        
        except Exception as e:
            raise SensorException(e, sys)     