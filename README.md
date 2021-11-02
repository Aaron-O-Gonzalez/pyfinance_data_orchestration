# pyfinance_data_orchestration
The following code is a small implementation of an Airflow-orchestrated retrieval of stock data from the pyfinance Python module. 

## Step 1: Configuration
The user is expected to perform a local installation of Apache Airflow. Importantly, the tasks are executed in parallel, which require that the user creates (1) a MySQL database backend and (2) use LocalExecutor:

For creation of a MySQL database:
    CREATE DATABASE airflow_db CHARACTER SET utf8;
    CREATE USER <user> IDENTIFIED BY <pass>;
    GRANT ALL PRIVILEGES ON airflow_db.* TO <user>;
    
To set the LocalExecutor, it is recommended that the user installs the PyMySQL connector and perform the following two changes in the **airflow.cfg** file:
    executor = LocalExecutor
    sql_alchemy_conn = mysql+pymysql://<user>:<pass>@localhost:3306/airflow_db

## Step 2: Dag Execution
<img src="https://github.com/Aaron-O-Gonzalez/pyfinance_data_orchestration/blob/master/stock_dag.png"/> 

The figure above summarizes the workflow for the tasks in the **dag.py** file. In short, a temporary folder, i.e., *data*, is created in the *tmp* directory; the pyFinance data for AAPL and TSLA stocks are loaded for 1 day, 1 minute intervals and written to CSV files; the CSV files are moved to the *data* directory; the data is read into a pandas dataframe, and the top 20 rows are displayed.

## Files
**dag.py**: Instantiates the tasks that will be needed for carrying out the DAG.
**plugins/ingest_stock_data**: Downloads the data based from the Pyfinance module based on stock ticker.
**plugins/query_stock_data**: As a quality control measure, loads the CSV files into a dataframe and presents the top 20 rows.
