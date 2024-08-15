from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from function import *
import os
from dotenv import load_dotenv

default_args ={
    'owner':'quangtp',
    'email':['quangtranphu0902@gmail.com'],
    'email_on_failure':True,
    'retries':5,
    'retries_delay':timedelta(minutes=2)
}

with DAG(
    dag_id = 'our_first_dag',
    default_args=default_args,
    description='This is our first dag',
    start_date=datetime(2024, 7, 13, 2),
    schedule_interval='@daily',
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo "Hello world, this is the first dag" >> test.txt'
    )

    task2 = PythonOperator(
        task_id = 'write_file',
        python_callable=write_file
    )

    task3 = PythonOperator(
        task_id='second_task',
        python_callable=send_email
    )

    task1 >> task2 >> task3