import smtplib
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from datetime import datetime
import openai  # Assuming OpenAI API is used for LLM
import os
import logging
from google.auth.transport.requests import Request
from google.auth import exceptions

# Load environment variables (Make sure to set these in your environment)
openai.api_key = os.getenv("OPENAI_API_KEY")
gmail_user = os.getenv("GMAIL_USER")
gmail_password = os.getenv("GMAIL_PASSWORD")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Send customized emails
def send_custom_emails(data, prompt):
    for row in data:
        try:
            custom_content = generate_email_content(prompt, row)
            send_email(row['Email'], custom_content)
            logging.info(f"Email sent to {row['Email']}")
        except Exception as e:
            logging.error(f"Failed to send email to {row['Email']}: {str(e)}")

# Generate content using LLM based on the prompt and row data
def generate_email_content(prompt, row):
    custom_prompt = prompt.format(**row)
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # Or use the latest GPT model available
            prompt=custom_prompt,
            max_tokens=150  # You can adjust this value depending on the email content length
        )
        return response.choices[0].text.strip()
    except openai.OpenAIError as e:
        logging.error(f"Error generating email content: {str(e)}")
        raise

# Send email through SMTP
def send_email(to_email, content):
    msg = MIMEText(content)
    msg['Subject'] = 'Customized Email'
    msg['From'] = gmail_user
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, to_email, msg.as_string())
    except smtplib.SMTPException as e:
        logging.error(f"Error sending email to {to_email}: {str(e)}")
        raise

# Get email stats for the dashboard
def get_email_stats():
    # Here you'd pull real-time stats from ESP (Email Service Provider), storing in a database or cache.
    return {"sent": 100, "pending": 10, "failed": 5}

# Example of how to use Google OAuth2 for Gmail (Optional Enhancement)
def authenticate_gmail_oauth():
    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.json'):
            creds = file.Storage('token.json').get()
        # If there are no (valid) credentials available, let the user log in.
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secrets.json', ['https://www.googleapis.com/auth/gmail.send'])
            creds = tools.run_flow(flow, file.Storage('token.json'))

        # Build the Gmail service
        service = build('gmail', 'v1', credentials=creds)

             # Use the service to send emails via Gmail API
        return service
    except exceptions.GoogleAuthError as e:
        logging.error(f"Error during Gmail OAuth authentication: {str(e)}")
        raise