import imaplib
import email
import json
from email_processor import EmailProcessor
from appointment_manager import AppointmentManager
from email_sender import EmailSender
import yaml

def fetch_emails():
    """Fetch unread emails from the inbox."""
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    mail = imaplib.IMAP4_SSL(config['email']['imap_server'])
    mail.login(config['email']['email_address'], config['email']['password'])
    
    mail.select('inbox')
    _, messages = mail.search(None, 'UNSEEN')
    
    for num in messages[0].split():
        _, msg = mail.fetch(num, '(RFC822)')
        email_body = msg[0][1]
        email_message = email.message_from_bytes(email_body)
        
        # Get email content
        if email_message.is_multipart():
            content = ''
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    content += part.get_payload(decode=True).decode()
        else:
            content = email_message.get_payload(decode=True).decode()
            
        yield {
            'from': email_message['from'],
            'subject': email_message['subject'],
            'content': content
        }

def main():
    """Main function to run the email scheduling agent."""
    email_processor = EmailProcessor()
    appointment_manager = AppointmentManager()
    email_sender = EmailSender()
    
    for email_data in fetch_emails():
        processed_request = json.loads(
            email_processor.process_email(email_data['content'])
        )
        
        slot = appointment_manager.find_available_slot(
            preferred_date=processed_request.get('preferred_date')
        )
        
        if slot:
            meet_link = email_sender.create_meet_link(
                slot['date'], 
                slot['start'], 
                slot['end']
            )
            
            email_sender.send_confirmation_email(
                email_data['from'],
                slot,
                meet_link
            )
            
            appointment_manager.book_appointment(
                slot['date'],
                slot['start']
            )

if __name__ == "__main__":
    main()