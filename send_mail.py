# Name: Tommy Cao
# Date: 12/10/19
# Company: GEVH
# Description: Rental booking feedback

import smtplib
from email.mime.text import MIMEText


def send_mail(customer, house, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '3e438884ecc40a'
    password = '15a5de18a881de'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>House: {house}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'tommylcao@gmail.com'
    receiver_email = 'gevh2880@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Booking Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
