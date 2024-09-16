# we will create a component (within training pipeline) for data evaluation
# this file is inline with "data_ingestion.py" file inside the "components" folder

from sensor.predictor import ModelResolver
from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import load_object
from sklearn.metrics import f1_score
import pandas  as pd
import os
import sys
from sensor.config import TARGET_COLUMN

class ModelEvaluation:
    # "model_eval_config" is the input to the "Model Evaluation" component            
    # "model_eval_config" is of type- (file name. data type) 'config_entity.ModelEvaluationConfig'
    # also, the output of "model trainer" phase -- ie "model_trainer_artifact" -- is the input to "model evaluation" phase
    # "model_trainer_artifact" is of the type "artifact_entity.ModelTrainerArtifact"

    # also, the output of "data ingestion" phase -- ie "data_ingestion_artifact" -- is the input to "model evaluation" phase
    # "data_ingestion_artifact" is of the type "artifact_entity.DataIngestionArtifact"
    # also, the output of "data transformation" phase -- ie "data_transformation_artifact" -- is the input to "model evaluation" phase
    # "data_transformation_artifact" is of the type "artifact_entity.DataTransformationArtifact"
    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact      
        ):
        try:
            logging.info(f"{'>>'*20}  model evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()

        except Exception as e:
            raise SensorException(e,sys)


    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            # if "saved_model" folder has model, then we will compare which model is best
            logging.info("if saved model folder has model the we will compare which model is best")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None: 
                # if latest_dir_path is None => there is no model
                # ie there is nothing to compare and we will just prepare the artifact details
                # ie from the  file "artifact_entity.py" inside the "entity" folder
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact

            # finding location of latest model, transformer and target encoder
            # ie the LATEST objects from the "saved_models" folder isnide the "sensor" folder
            logging.info("finding location of latest model, transformer and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            # previous trained objects ie transformer, model and target encoder
            # ie the LATEST objects from the "saved_models" folder isnide the "sensor" folder
            logging.info("previous trained objects of transformer, model and target encoder")
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)
            
            # currently trained model objects
            # ie the model which we just trained ie the mdodel which is in the training pipeline
            logging.info("currently trained model objects")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model  = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
            

            # now, we will do the comparison of the performance of both the models
            # we will do it for the test file ie we will use the "test.csv" file for this
            # we will use f1 score -- as it is a classification problem
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true =target_encoder.transform(target_df)
            
            # accuracy for the previous trained model 
            # ie the LATEST objects from the "saved_models" folder isnide the "sensor" folder
            # we will use f1 score -- as it is a classification problem
            input_feature_name = list(transformer.feature_names_in_)
            input_arr =transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            # we will use "inverse_transform" to get back our actual labels -- ie  "pos" class and "neg class"
            # because we had encoded "1" and "0" for "pos" class and "neg class"
            print(f"prediction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"accuracy using previous trained model: {previous_model_score}")
           
            # accuracy for the current trained model 
            # ie the model which we just trained ie the mdodel which is in the training pipeline
            # we will use f1 score -- as it is a classification problem
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true =current_target_encoder.transform(target_df)
            # we will use "inverse_transform" to get back our actual labels -- ie  "pos" class and "neg class"
            # because we had encoded "1" and "0" for "pos" class and "neg class"
            print(f"prediction using trained model: {current_target_encoder.inverse_transform(y_pred[:5])}")
            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"accuracy using current trained model: {current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info(f"current trained model is not better than previous model")
                raise Exception("current trained model is not better than previous model")

            # let us prepare the model evaluation artifact
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"model evaluation artifact: {model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise SensorException(e,sys)    