
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.predictor import ModelResolver
import pandas as pd
from sensor.utils import load_object
import os
import sys
from datetime import datetime
import numpy as np


PREDICTION_DIR="prediction"

# to do the prediction, we need to have our input file on which we will do the prediction
def start_batch_prediction(input_file_path):

    try:

        # we will create a folder/directory named as "prediction" -- where we will save all the
        # files related to prediction
        os.makedirs(PREDICTION_DIR,exist_ok=True)

        # we need model resolver -- so that we can load 
        # the 3 objects -- the files "transformer.pkl", "model.pkl" and "target_encoder.pkl" 
        logging.info(f"creating model resolver object")
        # we will pass that registry/folder where we have saved our 3 object files
        # ie we have saved them in "saved_models" folder  
        model_resolver = ModelResolver(model_registry="saved_models")

        logging.info(f"reading file :{input_file_path}")
        df = pd.read_csv(input_file_path)
        df.replace({"na":np.NAN},inplace=True)
        
        # (Here, do data validation if required) -- moving on.....


        logging.info(f"loading transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        # this part, we have written in the file "model_evaluation.py" inside the "components" folder
        input_feature_names =  list(transformer.feature_names_in_)
        # we want the 'input array'
        input_arr = transformer.transform(df[input_feature_names])

        logging.info(f"loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)
        
        logging.info(f"target encoder to convert predicted column into categorical")
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())

        cat_prediction = target_encoder.inverse_transform(prediction)

        # we will now update/fill in the -- "prediction" column (which was blank in the input df file)
        # and "cat_pred" column (which was blank in the input df file)
        # so, now our output file will have all the columns from the input file + filled columns of "prediction" and "cat_pred"
        df["prediction"]=prediction
        df["cat_pred"]=cat_prediction

        # prediction file name will be named like this
        # suppose input file name is "sensor1.csv", then
        # after prediciton, the output file name will be "sensor1_{timestamp}.csv"
        # ie "filename_{timestamp}.csv"
        # and this output file, we will save in the "prediction" folder
        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)

        # since our original input file was of ".csv", we will convert the output file
        # which is now a dataframe, into ".csv"
        # we dont want to keep the indexes    => index=False
        # we want to keep the column names    => header=True
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    
    except Exception as e:
        raise SensorException(e, sys)