import sys
import os

def error_message_detail(error, error_detail: sys):
    _,_, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

        # ie we will get -- from which file, which line number and what is the error
        # this will help us debug the errors in a better way
    error_message = "Error ocurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message



# we will create our own custom "exception" class --- called as "SensorException" class
# this is done so that we can debug the errors in a better way
# we have to inherit the standard "Exception" class inside our custom Exception class

class SensorException(Exception):     

    def __init__(self, error_message, error_detail: sys):
        self.error_message = error_message_detail(
            error_message, error_detail= error_detail
        )

    def __str__(self):
        return self.error_message   
        

        

