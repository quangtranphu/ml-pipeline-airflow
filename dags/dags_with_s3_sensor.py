from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'quangtp3',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}


with DAG(
    dag_id='dag_with_minio_s3_v09',
    start_date=datetime(2022, 2, 12),
    schedule_interval=None,
    default_args=default_args
) as dag:
    
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='ml-pipeline',
        bucket_key='datasets/bank-additional-full.csv',
        aws_conn_id='minio_s3_conn',
        mode="poke",
        poke_interval=5,
        timeout=30
    )

    model_train_and_publish_task = DockerOperator(
    task_id='docker_model_train_and_publish_task',
    docker_url="tcp://docker-socket-proxy:2375",  # Use the default Docker socket
    api_version='auto',  # Use 'auto' to let Docker select the appropriate API version
    auto_remove=True,  # Remove the container when the task completes
    image='classification-training-image:v1.0',  # Replace with your Docker image and tag
    container_name="training_my_awesome_model",
    environment={
        'MINIO_ENDPOINT': 'host.docker.internal:9000',
        'MINIO_ACCESS_KEY_ID': 'deEZp3GPDO6zeDCdx8Qf',
        'MINIO_SECRET_ACCESS_KEY': '', # secret key to minio
        'MINIO_BUCKET_NAME': 'ml-pipeline',
        'PASSWORD': ''  # app password to gmail
    },  # Set environment variables inside the contain
    network_mode='ml-pipeline-airflow_default',
    command=['python', 'model_training_script.py'],  # Replace with the command you want to run inside the container
    # network_mode='bridge',  # Specify the network mode if needed
    # volumes=['/host/path:/container/path'],  # Mount volumes if needed
    dag=dag,
    )

    task1 >> model_train_and_publish_task