from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_service():
    creds = service_account.Credentials.from_service_account_file(
        "cred.json",
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    return build("calendar", "v3", credentials=creds)

def check_availability():
    # Dummy for now
    return "You're available tomorrow 4PM - 5PM"

def book_event(title="Meeting", start="2025-07-06T16:00:00", end="2025-07-06T17:00:00"):
    service = get_service()
    event = {
        "summary": title,
        "start": {"dateTime": start, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end, "timeZone": "Asia/Kolkata"}
    }
    service.events().insert(calendarId="primary", body=event).execute()
    return f"Event '{title}' booked from {start} to {end}"
