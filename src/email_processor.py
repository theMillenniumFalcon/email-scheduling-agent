import os
from openai import OpenAI
import yaml

class EmailProcessor:
    def __init__(self):
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = config['openai']['model']
        
    def process_email(self, email_content):
        system_prompt = """
        You are an AI assistant that analyzes emails requesting appointments.
        Extract the following information:
        1. Type of appointment requested
        2. Preferred dates and times (if mentioned)
        3. Any special requirements or notes
        
        Format the response as JSON.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_content}
            ]
        )
        
        return response.choices[0].message.content