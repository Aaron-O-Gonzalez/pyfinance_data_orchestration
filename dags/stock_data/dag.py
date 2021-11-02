from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
import os
import sys
#sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))
from ingest_stock_data import download_stock_data
from query_stock_data import query_data

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes =5),
    'depends_on_past': False,
    'start_date': datetime(2021,10,28,18)
}

dag = DAG(dag_id='marketvol', default_args=default_args, description = 'data collection', schedule_interval='0 18 * * 1-5')

make_data_directory = BashOperator(
    task_id = 'make_data_directory',
    bash_command = 'mkdir -p /tmp/data/$(date +"%d-%m-%Y")',
    dag = dag
)

ingest_TSLA_data = PythonOperator(
    task_id = 'download_TSLA_data',
    python_callable=download_stock_data,
    op_kwargs={'stock_symbol': 'TSLA'},
    dag=dag
)

ingest_AAPL_data = PythonOperator(
    task_id = 'download_AAPL_data',
    python_callable=download_stock_data,
    op_kwargs={'stock_symbol': 'AAPL'},
    dag=dag
)

move_to_data_dir_AAPL = BashOperator(
    task_id='move_AAPL_to_data_dir',
    bash_command='mv /Users/aarongonzalez/Desktop/airflow_tutorial_3/AAPL_data.csv /tmp/data/$(date +"%d-%m-%Y")',
    dag=dag
)

move_to_data_dir_TSLA = BashOperator(
    task_id='move_TSLA_to_data_dir',
    bash_command='mv /Users/aarongonzalez/Desktop/airflow_tutorial_3/TSLA_data.csv /tmp/data/$(date +"%d-%m-%Y")',
    dag=dag
)

query_AAPL_data = PythonOperator(
    task_id = 'query_AAPL_data',
    python_callable=query_data,
    op_kwargs={'datafile_path': '/tmp/data/$(date +"%d-%m-%Y")/AAPL_data.csv'},
    dag=dag
)

query_TSLA_data = PythonOperator(
    task_id = 'query_TSLA_data',
    python_callable=query_data,
    op_kwargs={'datafile_path': '/tmp/data/$(date +"%d-%m-%Y")/TSLA_data.csv'},
    dag=dag
)

make_data_directory >> ingest_TSLA_data
make_data_directory >> ingest_AAPL_data

ingest_TSLA_data >> move_to_data_dir_TSLA
ingest_AAPL_data >> move_to_data_dir_AAPL

move_to_data_dir_TSLA >> query_TSLA_data

move_to_data_dir_AAPL >> query_AAPL_data

