# APS-Sensor-Fault-Detection

Hello, welcome to the project!

### Problem Statement 
The Mechanical Engineering Department of a vehicle company has designed a new type of braking system which uses some kind of "Air Pressure System (APS)”, and this system has multiple sensors integrated within it. The readings of these sensors are available. It is given that there is a failure in a particular vehicle. Now, based on the readings of the sensors, it is to be determined whether the failure is due to the APS. <br>
Clearly, it is a BINARY CLASSIFICATION problem statement in Machine Learning. <br>

### Initial files availabe 
Data file - "aps_failure_training_set1.csv" <br>
Requirements for the environment - "requirements.txt" <br>

### What was done in the project?
•	Designed the complete Training Pipeline (which consists of these components - Data Ingestion, Data Validation, Data Transformation, Model Trainer, Model Evaluation, Model Pusher) <br>
•	Incorporated scope for Re-Training or Continuous Training <br>
•	Performed various experiments on the dataset and concluded that - XGBoostClassifier algorithm using Simple Imputer with strategy “constant” has performed the best <br>
•	Designed the Prediction Pipeline (To obtain the Batch Prediction File) <br>

### To run the Training Pipeline 
Open VS Code <br>
Locate the folder to the project <br>
Run the "main.py" file <br>

### To run the Batch Prediction Pipeline
Get the input file on which the prediction is to be done <br>
(For now, assume that it is the file - "aps_failure_training_set1.csv") <br>
Open VS Code <br>
Locate the folder to the project <br>
Run the "run_prediction.py" file <br>

Hope you liked the project!
