# Database Schema Migration Guide

## Summary of Changes

The club database schema has been updated to match the TerpLink CSV export format:

### Old Schema
- `id` (Integer, Primary Key)
- `name` (String, 255)
- `url` (String, 512)
- `description` (Text)
- `category` (String, 100) - Auto-categorized
- `meeting_times` (Relationship)

### New Schema
- `id` (Integer, Primary Key)
- `name` (String, 255)
- `website_url` (String, 512)
- `picture_id` (String, 255) - Optional
- `summary` (Text)
- `categories` (String, 500) - From CSV (comma-separated if multiple)
- `meeting_times` (Relationship)

## Migration Steps

### 1. Delete Old Database
```bash
cd backend
rm -f clubs.db
```

### 2. Reinitialize Database
```bash
flask init-db
```

### 3. Seed with Sample Data
```bash
flask seed-db
```

### 4. (Optional) Import from TerpLink CSV
```python
from app import app
from utils.db_seed import DatabaseSeeder
import pandas as pd

with app.app_context():
    # Read CSV from scraping folder
    df = pd.read_csv('../scraping/clubs.csv')
    
    # Convert to list of dictionaries
    clubs_data = []
    for _, row in df.iterrows():
        clubs_data.append({
            'name': row['Name'],
            'website_url': row['WebsiteKey'],  # or use the URL field
            'picture_id': row['ProfilePicture'],
            'summary': row['Summary'],
            'categories': row['CategoryNames'],
            'meeting_times': row['MeetingTimes'].split(';') if pd.notna(row['MeetingTimes']) else []
        })
    
    DatabaseSeeder.seed_from_data(clubs_data)
```

## API Response Changes

The API responses now include the new fields:

```json
{
  "id": 1,
  "name": "Computer Science Club",
  "website_url": "https://example.com/cs-club",
  "picture_id": "cs-club-pic.jpg",
  "summary": "A club for students interested in computer science and programming.",
  "categories": "Science and Technology",
  "meeting_times": [
    {
      "id": 1,
      "day_of_week": "Monday",
      "time_slot": "Morning",
      "meeting_description": "Monday Morning"
    }
  ]
}
```

## Notes

- **Categories are no longer auto-assigned** - They come from the CSV import
- **Picture IDs are now stored** for potential image lookups
- **URL changed from `url` to `website_url`** for clarity
- **Description changed to `summary`** to match CSV column names
- All meeting times still use the same format: "Day TimeSlot" (e.g., "Monday Morning")
