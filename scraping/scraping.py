import requests
import pandas as pd

def get_club_times(club_id):
    data = {}
    while "items" not in data:
        data = requests.get(f"https://terplink.umd.edu/api/discovery/organization/{club_id}/additionalFields").json()

    print(f"Club times retrieved for club w id: {club_id}")
    try:
        return [q["answerText"] for q in data["items"] if (q["questionId"] == 11487938 and q["hasResponse"])]
    except:
        print(data)

def format_times(times):
    """
    Transform TerpLink API time values to backend format (e.g., "Monday Morning")
    
    API time values can be:
    - Time periods: "Early Morning (before 9am)", "Morning (9am-12pm)", 
                    "Early Afternoon (12pm-3pm)", "Late Afternoon (3pm-6pm)", 
                    "Evening (6pm-9pm)", "Late Night (After 9pm)"
    - Day patterns: "Weekdays (Monday-Friday)", "Weekends (Saturday and Sunday)"
    
    Returns: List of formatted meeting time strings (e.g., ["Monday Morning", "Saturday Afternoon"])
    """
    if not times:
        return []
    
    # Map API time descriptions to backend time slots
    TIME_SLOT_MAP = {
        "early morning": "Morning",
        "morning": "Morning",
        "early afternoon": "Afternoon",
        "late afternoon": "Afternoon",
        "evening": "Evening",
        "late night": "Night",
    }
    
    # Days of the week for weekdays and weekends
    WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    WEEKEND_DAYS = ["Saturday", "Sunday"]
    
    # Determine which days and time slots apply
    days_to_use = []
    time_slots_to_use = []
    
    # Extract days (weekdays, weekends, or specific days)
    has_weekdays = any("weekday" in t.lower() for t in times)
    has_weekends = any("weekend" in t.lower() for t in times)
    
    if has_weekdays:
        days_to_use.extend(WEEKDAYS)
    if has_weekends:
        days_to_use.extend(WEEKEND_DAYS)
    
    # If no explicit day pattern, assume all days apply
    if not days_to_use:
        days_to_use = WEEKDAYS + WEEKEND_DAYS
    
    # Extract time slots from the API values
    for time_str in times:
        time_lower = time_str.lower()
        # Try to match against our time slot map
        for api_time, slot in TIME_SLOT_MAP.items():
            if api_time in time_lower:
                if slot not in time_slots_to_use:
                    time_slots_to_use.append(slot)
                break
    
    # If no time slots found, default to Afternoon
    if not time_slots_to_use:
        time_slots_to_use = ["Afternoon"]
    
    # Generate all combinations of days and time slots
    formatted_times = []
    for day in days_to_use:
        for time_slot in time_slots_to_use:
            formatted_times.append(f"{day} {time_slot}")
    
    return formatted_times

def fetch_club_times():
    df = pd.read_csv("clubs.csv")
    df["MeetingTimes"] = df["Id"].apply(get_club_times)
    df["MeetingTimes"] = df["MeetingTimes"].apply(format_times)
    df.to_csv("clubs.csv")