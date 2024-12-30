from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import sys
from pathlib import Path

src_path = str(Path(__file__).parent.parent / 'src')
sys.path.append(src_path)

SCOPES = ['https://www.googleapis.com/auth/calendar']

def test_calendar_setup():
    creds = None
    credentials_path = Path(__file__).parent.parent / 'credentials.json'
    token_path = Path(__file__).parent.parent / 'token.json'
    
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path), SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', 
                                            timeMin=now,
                                            maxResults=10, 
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        if not events:
            print('No upcoming events found.')
            return
            
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"Event: {event['summary']}, Start: {start}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    test_calendar_setup()