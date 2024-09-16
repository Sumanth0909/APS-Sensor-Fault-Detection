# -------------------------------------------------------------------------------------------------
# (A)
from sensor.logger import logging
from sensor.exception import SensorException

import sys


def test_logger_and_exception():
    try:
        logging.info("Starting the test_logger_and_exception")
        result = 3/0
        print(result)
        logging.info("Stopping the test_logger_and_exception")

    except Exception as e:
        logging.debug(str(e))

        raise SensorException(e, sys)
    

if __name__ == "__main__":
    try:
        test_logger_and_exception()

    except Exception as e:
        print(e)    

# this was just a demonstration of how we get our custom exceptions - just see the error message
# we are able to see the exact line number where there is error and what is the error   
# also, we can see that the particular log files are created     

# ---------------------------------------------------------------------------------------------------

# (B)

# to test/see whether our logger and exceptions is working fine or not
# wrt the "utils.py" file -- (B) part 
# ie whether we are able to log whenever we are getting the data from MongoDB as a  dataframe
# by using 'get_collection_to_dataframe' function
import sensor.utils

if __name__ == "__main__":
    try:
        get_collection_as_dataframe(database_name = "aps", collection_name = "sensor")
        
    except Exception as e:
        print(e)    
# ----------------------------------------------------------------------------------------------------
# Now, the real usage of this "main.py" file starts 



from sensor.pipeline.training_pipeline import start_training_pipeline

print(__name__)
if __name__=="__main__":
     try:
          
          # we will start the training pipeline
          # we will call the "start_training_pipeline()" from the file "training_pipeline.py" inside the "pipeline" folder
          start_training_pipeline()

     except Exception as e:
          print(e)

