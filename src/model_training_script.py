import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from minio import Minio
from minio.error import S3Error
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
from sklearn.metrics import roc_auc_score, roc_curve, auc
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# Configure the MinIO client with your MinIO server details
minio_client = Minio(
    endpoint='localhost:9000',  # Replace with your MinIO server address and port
    access_key=os.environ.get('MINIO_ACCESS_KEY_ID'),
    secret_key=os.environ.get('MINIO_SECRET_ACCESS_KEY'),
    secure=False,  # Set to True if using HTTPS
)

# Define the bucket name and object key for the data.csv file
bucket_name = os.environ.get('MINIO_BUCKET_NAME')
data_csv_key = "datasets/bank-additional-full.csv"

# Download the data.csv file from MinIO
try:
    minio_client.fget_object(bucket_name, data_csv_key, "bank-additional-full.csv")
    print(f"Downloaded data.csv from MinIO: s3://{bucket_name}/{data_csv_key}")
except S3Error as e:
    print(f"Error downloading data.csv from MinIO: {e}")

# Load your dataset from the downloaded CSV file
data = pd.read_csv(".//bank-additional-full.csv", delimiter=";")

# Train, test split
data['y'] = np.where(data['y']=='yes', 1, 0)

# set seed
seed = 123
test_size = 0.2

train, test = train_test_split(data, test_size=test_size,
                               random_state=seed,
                               stratify=data['y'])

model_col = ['age', 'campaign', 'pdays',
             'previous', 
             'emp.var.rate',
             'cons.price.idx', 
             'cons.conf.idx',
             'euribor3m',
             'nr.employed']

x_train =  train[model_col]
y_train = train['y']

clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)

# Prediction on test set
x_test = test[model_col]
y_test = test['y']

y_pred = clf.predict_proba(x_test)

fpr, tpr, threshold = roc_curve(y_test, y_pred[:,1])
roc_auc = auc(fpr, tpr)

msg = f"Model AUC: {roc_auc}"

with open("model_metrics.txt", "w") as file:
    file.write(msg)
    file.close

smtp_port = 587
smtp_server = 'smtp.gmail.com'
email_from = 'quangtranphu0902@gmail.com'
email_to = 'quangtranphu0902@gmail.com'
passwd= 'tkrk oiwq yzau mwqg'
subject= 'From quangtp with test'

def send_email(file_name, message):
    body = message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    file_name = file_name

    attachment= open(file_name, 'rb')  # r for read and b for binary

    # Encode as base 64
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + file_name)
    msg.attach(attachment_package)

    # Cast as string
    text = msg.as_string()

    # Connect with the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(os.environ['SMTP_SERVER'], os.environ['SMTP_PORT'])
    TIE_server.starttls()
    TIE_server.login(email_from, os.environ['PASSWORD'])
    print("Succesfully connected to server")
    print()


    # Send emails to "person" as list is iterated
    print(f"Sending email to: {email_to}...")
    TIE_server.sendmail(email_from, email_to, text)
    print(f"Email sent to: {email_to}")
    print()

    # Close the port
    TIE_server.quit()

send_email(file_name='model_metrics.txt',
           message=f"""Đây là kết quả model:
AUC: {roc_auc}
""")