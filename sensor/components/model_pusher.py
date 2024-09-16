# we will create a component (within training pipeline) for data pusher
# this file is inline with "data_ingestion.py" file inside the "components" folder

from sensor.predictor import ModelResolver
from sensor.entity.config_entity import ModelPusherConfig
from sensor.exception import SensorException
import os
import sys
from sensor.utils import load_object
from sensor.utils import save_object
from sensor.logger import logging
from sensor.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ModelPusherArtifact

class ModelPusher:

    # "model_pusher_config" is the input to the "Model Pusher" component            
    # "model_pusher_config" is of type- (file name. data type) 'config_entity.ModelPusherConfig'
    # also, the output of "model trainer" phase -- ie "model_trainer_artifact" -- is the input to "model evaluation" phase
    # "model_trainer_artifact" is of the type "artifact_entity.ModelTrainerArtifact"

    # also, the output of "data transformation" phase -- ie "data_transformation_artifact" -- is the input to "model trainer" phase
    # "data_transformation_artifact" is of the type "artifact_entity.DataTransformationArtifact"
    def __init__(self,model_pusher_config:ModelPusherConfig,
    data_transformation_artifact:DataTransformationArtifact,
    model_trainer_artifact:ModelTrainerArtifact):
        try:

            # 
            logging.info(f"{'>>'*20} data transformation {'<<'*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise SensorException(e, sys)
        
def initiate_model_pusher(self,)->ModelPusherArtifact:
        
        try:

            # let us load the transformer, model and target encoder files
            logging.info(f"loading the objects ie transformer, model and target encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            # let us save the objects into 'model_pusher' directory
            logging.info(f"saving the objects into 'model_pusher' directory")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, obj=model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, obj=target_encoder)

            # let us save the objects in 'saved_models' dir
            # first we will get the location where we need to save them
            # here, we will get the location only ; no folders are created
            logging.info(f"saving the objects in 'saved_models' dir")
            transformer_path=self.model_resolver.get_latest_save_transformer_path()
            model_path=self.model_resolver.get_latest_save_model_path()
            target_encoder_path=self.model_resolver.get_latest_save_target_encoder_path()

            # let us save the objects
            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)
            save_object(file_path=target_encoder_path, obj=target_encoder)

            # let us prepare the model pusher artifact
            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                          saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)        