from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.dummy import DummyOperator
import logging


dag_version = "dev-44c9e09"


try:
    # dag_ids is a Python dict object. Do not treat as a JSON object 
    dag_ids = Variable.get("dags_version", default_var="Error with dags_version Airflow variable", deserialize_json=True)
    logging.info("Fetched DAG ids from Airflow env variable: {}".format(str(dag_ids)))

except Exception as e:
    logging.error("Error when fetching dags_version variable from Airflow: {}".format(str(e)))

reload_audit_table=f"SELECT 'Execute audit table procedure';"

default_args = {
    'owner': 'master',
    'schedule':"0 4 * * *",
    'depends_on_past': False,
    'retries': 1, # Unlike rest of the DAGs, master dag has no automatic retries
}


with DAG(dag_ids["master"],
default_args=default_args,
start_date= datetime(2025,3,12),
catchup=False,
max_active_runs=1,
schedule='0 4 * * *') as dag:
    
    Groups_process_ = TriggerDagRunOperator(
        task_id = 'groups_process',
        trigger_dag_id=dag_ids["groups"], 
        wait_for_completion=True,
        deferrable=True,
        dag=dag,
    )

    Users_process_ = TriggerDagRunOperator(
        task_id = 'users_process',
        trigger_dag_id=dag_ids["users"],
        wait_for_completion=True,
        deferrable=True,
        dag=dag,
    )

    
    reload_audit_table_ = BigQueryInsertJobOperator(
        task_id='reload_audit_table',
        configuration={
            "query": {
                "query": reload_audit_table,
                "use_legacy_sql": False,
            },
        },
    )

    Customers_process_ = TriggerDagRunOperator(
        task_id = 'customers_process',
        trigger_dag_id=dag_ids["customers"],
        wait_for_completion=True,
        deferrable=True,
        dag=dag,
    )

    Groups_process_ >> Users_process_ >> reload_audit_table_ >> Customers_process_
