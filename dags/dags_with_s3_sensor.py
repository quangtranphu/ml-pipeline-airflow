from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


default_args = {
    'owner': 'quangtp3',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}


with DAG(
    dag_id='dag_with_minio_s3_v02',
    start_date=datetime(2022, 2, 12),
    schedule_interval=None,
    default_args=default_args
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='ml-pipeline',
        bucket_key='datasets/bank-additional-full.csv',
        aws_conn_id='minio_conn',
        mode="poke",
        poke_interval=5,
        timeout=30
    )