import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

class EmailService:
    def __init__(self, app=None):
        self.sg = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app context"""
        api_key = app.config.get('SENDGRID_API_KEY')
        if not api_key:
            print("Warning: SendGrid not configured - missing API key")
            return
        self.sg = SendGridAPIClient(api_key)

    def send_email(self, to_email, subject, html_content):
        if not self.sg:
            print("Error: SendGrid not configured")
            return False
            
        message = Mail(
            from_email='noreply@vendorsync.com',  # Replace with your verified sender
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        try:
            response = self.sg.send(message)
            print(f"SendGrid Status Code: {response.status_code}")
            return response.status_code in [200, 202]
        except Exception as e:
            print(f"Error sending email: {e}")
            return False