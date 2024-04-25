import smtplib, os, json
from email.message import EmailMessage


def notify(body):
    message = json.loads(body)
    sender_address = os.environ.get("SENDER_ADDRESS")
    sender_password = os.environ.get("SENDER_PASS")
    receiver_address = message["username"]
    
    mail = EmailMessage()
    mail["subject"] = "Your audio file is ready.."
    mail["From"] = sender_address
    mail["To"] = receiver_address
    
    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(mail, sender_address, receiver_address)
    session.quit()
    
    
    