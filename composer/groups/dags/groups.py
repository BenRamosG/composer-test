from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.models.variable import Variable
from datetime import datetime
from airflow import DAG
import requests
import time
import json
import os

print(12)
dag_version = "4.0.7"

args = {
     'retries': 3,
     'owner': "groups"
}



with DAG("groups",
         start_date= datetime(2025,3,8),
         schedule= "0 4 * * *",
         catchup= False,
         default_args= args,
         max_active_runs = 1
         ) as dag:
         
         
         
     start = DummyOperator(task_id= "init")


     sleep_task = BashOperator(
        task_id="sleep_task",
        bash_command="sleep 10",
        dag=dag,
    )



start >> sleep_task



