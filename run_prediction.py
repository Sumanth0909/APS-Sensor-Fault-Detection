# this file will be used to run the batch prediction pipeline

from sensor.logger import logging
from sensor.exception import SensorException

from sensor.pipeline.batch_prediction import start_batch_prediction

# give the input file path -- for the predicion
# ie give the file path for the input file on which we want to do the prediction
# for now, we will use the same file -- as input file -- on which we will do the prediction
file_path="/config/workspace/aps_failure_training_set1.csv"

print(__name__)
if __name__=="__main__":
     
    try:
          
          # we will start the batch prediction pipeline
          # we will call the "start_batch_prediction()" from the file "batch_prediction.py" inside the "pipeline" folder
          output_file = start_batch_prediction(input_file_path=file_path)
          print(output_file)

    except Exception as e:
          print(e)      
          