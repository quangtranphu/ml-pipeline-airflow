from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart

email_from = 'quangtranphu0902@gmail.com'
email_to = 'quangtranphu0902@gmail.com'
subject= 'Test email from dag'

def send_email(file_name, **kwargs):
    body = """
    Đây là Email test
    From quangtp
    """
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
    TIE_server = smtplib.SMTP('smtp.gmail.com', 587)
    TIE_server.starttls()
    TIE_server.login(email_from, 'tkrk oiwq yzau mwqg')
    print("Succesfully connected to server")
    print()


    # Send emails to "person" as list is iterated
    print(f"Sending email to: {email_to}...")
    TIE_server.sendmail(email_from, email_to, text)
    print(f"Email sent to: {email_to}")
    print()

    # Close the port
    TIE_server.quit()

def write_file(file_name, **kwargs):
    with open(f"./{file_name}", "wb") as file:
        file.write('Đưa hết tiền đây'.encode())