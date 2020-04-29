from flask_mail import Message
from flask import url_for, render_template

from app.token import generate_confirmation_token
from app import app, mail

def send_new_confirmation_token(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('users/activate.html', confirm_url=confirm_url)
    subject = "Confirm your email to create your Spot account"
    send_email(email, subject, html)

def send_listing_cancellation_confirmation(email, pet_name):
    html = render_template('users/listing_cancellation.html', petName = pet_name)
    subject = "[Spot] Confirmation on your cancelled listing."
    send_email(email, subject, html)



# Sends an email to a single recipient "to" with subject *subject* and template *template*
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)