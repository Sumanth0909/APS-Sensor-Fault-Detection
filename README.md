# APS-Sensor-Fault-Detection

Hello, welcome to the project!

### Problem Statement 
The Mechanical Engineering Department of a vehicle company has designed a new type of braking system which uses some kind of "Air Pressure System (APS)”, and this system has multiple sensors integrated within it. The readings of these sensors are available. It is given that there is a failure in a particular vehicle. Now, based on the readings of the sensors, it is to be determined whether the failure is due to the APS.
Clearly, it is a BINARY CLASSIFICATION problem statement in Machine Learning. 

### Initial files availabe 
Data file - "aps_failure_training_set1.csv"
Requirements for the environment - "requirements.txt"

### What was done in the project?
•	Designed the complete Training Pipeline (which consists of these components - Data Ingestion, Data Validation, Data Transformation, Model Trainer, Model Evaluation, Model Pusher)
•	Incorporated scope for Re-Training or Continuous Training 
•	Performed various experiments on the dataset and concluded that - XGBoostClassifier algorithm using Simple Imputer with strategy “constant” has performed the best
•	Designed the Prediction Pipeline (To obtain the Batch Prediction File)

### To run the Training Pipeline 
Open VS Code
Locate the folder to the project
Run the "main.py" file

### To run the Batch Prediction Pipeline
Get the input file on which the prediction is to be done 
(For now, assume that it is the file - "aps_failure_training_set1.csv")
Open VS Code
Locate the folder to the project
Run the "run_prediction.py" file

Hope you liked the project!
