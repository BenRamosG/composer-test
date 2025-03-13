from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.operators.dummy import DummyOperator


reload_audit_table=f"SELECT 'Execute audit table procedure';"

default_args = {
    'owner': 'THDP-TIR',
    'schedule':"0 4 * * *",
    'depends_on_past': False,
    'retries': 1, # Unlike rest of the DAGs, master dag has no automatic retries
}


child_dags_ids = {} # Fetch these from the other dag files

with DAG("master_dag",
default_args=default_args,
catchup=False,
max_active_runs=1,
schedule='0 4 * * *') as dag:
    
    Groups_process_ = TriggerDagRunOperator(
        task_id = 'groups_process',
        trigger_dag_id="groups" + "_" + "1.0.11", # Replace for child_dags_ids{"groups"} 
        wait_for_completion=True,
        deferrable=True,
        dag=dag,
    )

    Users_process_ = TriggerDagRunOperator(
        task_id = 'users_process',
        trigger_dag_id="users" + "_" + "1.0.3", # Replace for child_dags_ids{"users"}
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
        trigger_dag_id="customers" + "_" + "1.1.4", # Replace for child_dags_ids{"customers"}
        wait_for_completion=True,
        deferrable=True,
        dag=dag,
    )

    Groups_process_ >> Users_process_ >> reload_audit_table_ >> Customers_process_
