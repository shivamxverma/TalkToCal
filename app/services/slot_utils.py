from datetime import datetime, timedelta

def generate_time_slots(start_date: datetime, booked_slots: list):
    current_time = start_date.replace(hour=9, minute=0)
    end_time = start_date.replace(hour=17, minute=0)
    available = []
    while current_time < end_time:
        slot_str = current_time.strftime("%Y-%m-%dT%H:%M:%S")
        if slot_str not in booked_slots:
            available.append(slot_str)
        current_time += timedelta(minutes=30)
    return available
