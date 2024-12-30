import json

class AppointmentManager:
    def __init__(self, appointments_file='data/appointments.json'):
        self.appointments_file = appointments_file
        
    def load_appointments(self):
        """Load available appointments from JSON file."""
        with open(self.appointments_file, 'r') as f:
            return json.load(f)
        
    def find_available_slot(self, preferred_date=None):
        """Find next available appointment slot."""
        appointments = self.load_appointments()
        
        for day in appointments['available_slots']:
            if preferred_date and day['date'] != preferred_date:
                continue
                
            for slot in day['slots']:
                if slot['available']:
                    return {
                        'date': day['date'],
                        'start': slot['start'],
                        'end': slot['end']
                    }
        
        return None
        
    def book_appointment(self, date, start_time):
        """Mark an appointment slot as booked."""
        appointments = self.load_appointments()
        
        for day in appointments['available_slots']:
            if day['date'] == date:
                for slot in day['slots']:
                    if slot['start'] == start_time:
                        slot['available'] = False
                        
        with open(self.appointments_file, 'w') as f:
            json.dump(appointments, f, indent=2)