from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import json


def notify(body):
    body = json.loads(body)
    sender_login = os.environ.get("MAILTRAP_USERNAME")
    sender_address = 'mailtrap@demomailtrap.com'
    sender_password = os.environ.get("MAILTRAP_PASS")
    receiver_address = body["username"]

    subject = "Your audio file is ready.."
    html = f"""\
    <html>
    <body>
        <p>Hi,<br>        
        <a href="http://mp3converter.com/v1/download?fid={body['mp3_fid']}">Download audio</a>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = body["username"]
    message["Subject"] = subject

    message.attach(MIMEText(html, "html"))
    session = smtplib.SMTP("live.smtp.mailtrap.io", 587)
    session.starttls()
    session.login(sender_login, sender_password)
    session.sendmail(sender_address, receiver_address, message.as_string())
    session.quit()
