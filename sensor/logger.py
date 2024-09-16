# logger is used to log each and every executions

import logging
import os
from datetime import datetime
import os

LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"
# ('%d%m%Y__%H%M%S') = month_month_year__hour_min_sec    format
# ie we will be creating "log files" which is named based on at what time(/when) an execution happens
# example - if I execute a file on 9th sept 1997 at 11 25 am, then 
# that particular log file will be named as "09091997__112500"
# everytime you run/execute, it will create a new log file - based on "the time then"

LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")
 # this is the directory where the log files are stored
 #os.getcwd() = gives current directory
 # we are creating a new directory/folder named as "logs"

os.makedirs(LOG_FILE_DIR,exist_ok=True)  # exist_ok=True) -- if folder is already available, then dont
                                         #                   create a new one again 
# os.makedirs(LOG_FILE_DIR -- used to create the directory "in actually"
# LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")-was used just to define, but no actual creation took 


# log file path
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)


# basic config is a function for doing basic configuration of the log -
# ie if you want to configure your log for the project, you can do it using basic config function
# in this, you have to specify "in which folder" you will create log (ie filename)
# and then, specify "how will the log message be displayed" (ie format)
# and then, "log level" (we have 6 levels in logging - notset, debug, info, warning, error, critical)
logging.basicConfig(
    filename= LOG_FILE_NAME,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO,
)

