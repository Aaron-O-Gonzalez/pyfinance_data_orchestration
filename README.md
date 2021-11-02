# pyfinance_data_orchestration
The following code is a small implementation of an Airflow-orchestrated retrieval of stock data from the pyfinance Python module. 

## Step 1: Configuration
The user is expected to perform a local installation of Apache Airflow. Importantly, the tasks are executed in parallel, which require that the user creates (1) a MySQL database backend and (2) use LocalExecutor:

    CREATE DATABASE airflow_db CHARACTER SET utf8;
    CREATE USER <user> IDENTIFIED BY <pass>;
    GRANT ALL PRIVILEGES ON airflow_db.* TO <user>;
    
