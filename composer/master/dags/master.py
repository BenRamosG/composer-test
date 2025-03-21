
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


dag_version = "default"


args = {
     'retries': 3,
     'owner': "groups"
}



with DAG(f"master_dag_{dag_version}",
         start_date= datetime(2025,3,8),
         schedule= "0 4 * * *",
         catchup= False,
         default_args= args,
         max_active_runs = 1
         ) as dag:
         
         
    Reference_process_ = TriggerDagRunOperator(
    task_id='reference_process',
    trigger_dag_id=f"reference_process_{dag_ids["reference_load"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    Pharmacy_process_ = TriggerDagRunOperator(
    task_id='pharmacy_process',
    trigger_dag_id=f"pharmacy_process_{dag_ids["pharmacy_process"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    Provider_process_ = TriggerDagRunOperator(
    task_id='provider',
    trigger_dag_id=f"provider_{dag_ids["provider"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    Groups_ = TriggerDagRunOperator(
    task_id='groups',
    trigger_dag_id=f"groups_{dag_ids["groups_process"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    Diseases_Products_Process_ = TriggerDagRunOperator(
    task_id='diseases_products_process',
    trigger_dag_id=f"diseases_products_process_{dag_ids["diseases_products"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    cardholders_process_ = TriggerDagRunOperator(
    task_id='cardholders_process',
    trigger_dag_id=f"cardholders_process_{dag_ids["cardholders_process"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    paid_claim_process_ = TriggerDagRunOperator(
    task_id='paid_claim_process',
    trigger_dag_id=f"paid_claim_process_{dag_ids["paid_claim_process"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    olap_process_ = TriggerDagRunOperator(
    task_id='olap_process',
    trigger_dag_id=f"olap_process_{dag_ids["olap_process"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )


    DW_Segment_Process_ = TriggerDagRunOperator(
    task_id='dw_segment_process',
    trigger_dag_id=f"dw_segment_process_{dag_ids["dw_segment"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    Batch_IQVIA_Claim_Extract_Process_ = TriggerDagRunOperator(
    task_id='batch_iqvia_claim_extract',
    trigger_dag_id=f"batch_iqvia_claim_extract_{dag_ids["batch_iqvia_claim_extract"]}",
    wait_for_completion=True,
    deferrable=True,
    dag=dag,
    )

    Reference_process_ >> Pharmacy_process_ >> Provider_process_ >> Groups_ >> Diseases_Products_Process_ >> cardholders_process_
    cardholders_process_ >> paid_claim_process_ >> olap_process_
    cardholders_process_ >> DW_Segment_Process_ >> Batch_IQVIA_Claim_Extract_Process_
