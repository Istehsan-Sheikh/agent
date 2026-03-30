from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "credentials.json"
CALENDAR_ID = os.getenv("CALENDAR_ID")

def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=creds)
    return service

def check_availability(date_str, time_str):
    service = get_calendar_service()
    
    dt_start = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    dt_end = dt_start + timedelta(hours=1)
    
    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=dt_start.isoformat() + "Z",
        timeMax=dt_end.isoformat() + "Z",
        singleEvents=True
    ).execute()
    
    existing = events.get("items", [])
    
    if len(existing) >= 3:
        return False
    return True

def add_appointment(name, phone, doctor, date_str, time_str):
    service = get_calendar_service()
    
    dt_start = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    dt_end = dt_start + timedelta(hours=1)
    
    event = {
        "summary": f"{name} - {doctor}",
        "description": f"Patient: {name}\nPhone: {phone}\nDoctor: {doctor}",
        "start": {"dateTime": dt_start.isoformat(), "timeZone": "America/Chicago"},
        "end": {"dateTime": dt_end.isoformat(), "timeZone": "America/Chicago"},
    }
    
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"Appointment confirmed for {name} with {doctor} on {date_str} at {time_str}"