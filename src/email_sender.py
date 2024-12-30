import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class EmailSender:
    def __init__(self):
        with open('config/config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.email = self.config['email']['email_address']
        self.password = self.config['email']['password']
        self.smtp_server = self.config['email']['smtp_server']
        self.smtp_port = self.config['email']['smtp_port']
        
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = self._get_google_credentials(SCOPES)
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)
        
    def _get_google_credentials(self, SCOPES):
        """Get or refresh Google API credentials."""
        creds = None
        if os.path.exists(self.config['google']['token_file']):
            creds = Credentials.from_authorized_user_file(
                self.config['google']['token_file'], SCOPES)
        
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.config['google']['credentials_file'], SCOPES)
            creds = flow.run_local_server(port=0)
            
            with open(self.config['google']['token_file'], 'w') as token:
                token.write(creds.to_json())
                
        return creds
        
    def create_meet_link(self, date, start_time, end_time):
        """Create a Google Meet link for the appointment."""
        event = {
            'summary': 'Appointment',
            'start': {
                'dateTime': f'{date}T{start_time}:00',
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': f'{date}T{end_time}:00',
                'timeZone': 'UTC',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f'appointment-{date}-{start_time}',
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            }
        }
        
        event = self.calendar_service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()
        
        return event['hangoutLink']
        
    def send_confirmation_email(self, to_email, appointment_details, meet_link):
        """Send confirmation email with appointment details and Meet link."""
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = "Appointment Confirmation"
        
        body = f"""
        Your appointment has been confirmed for:
        Date: {appointment_details['date']}
        Time: {appointment_details['start']} - {appointment_details['end']}
        
        Join the meeting using this link:
        {meet_link}
        
        Please let us know if you need to reschedule.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)