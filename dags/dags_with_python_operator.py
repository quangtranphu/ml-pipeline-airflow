from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from function import *

smtp_port = 587
smtp_server = 'smtp.gmail.com'

email_from = 'quangtranphu0902@gmail.com'
email_to = 'quangtranphu0902@gmail.com'

passwd= 'tkrk oiwq yzau mwqg'

subject= 'test dag'

default_args = {
    'owner': 'quangtp3',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dags_with_python_operator_v18',
    default_args=default_args,
    start_date=datetime(2024, 8, 6),
    schedule_interval='@yearly'
) as dag:
    task1 = PythonOperator(
        task_id='send_email',
        python_callable=send_email,
        op_kwargs={'file_name':'test1.txt'},
        dag=dag
    )

    task2 = PythonOperator(
        task_id = 'write_file',
        python_callable=write_file,
        op_kwargs={'file_name':'test1.txt'}
    )

    task2 >> task1