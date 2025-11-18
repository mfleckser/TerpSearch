# TerpSearch Backend

Flask-based REST API server for the TerpSearch club discovery application.

## Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file** (optional)
```bash
cp .env.example .env
```

## Running the Server

### Initialize Database
```bash
flask init-db
```
This creates the SQLite database (`clubs.db`) and initializes all tables.

### Seed with Sample Data
```bash
flask seed-db
```
This populates the database with 5 sample clubs (defined in `app.py`).

### Alternatively, load from CSV or JSON
```bash
# From Python shell
from app import app
from utils.db_seed import DatabaseSeeder

with app.app_context():
    # Load from CSV
    DatabaseSeeder.seed_from_csv('sample_clubs.csv')
    
    # OR load from JSON
    DatabaseSeeder.seed_from_json('sample_clubs.json')
```

### Development Mode (with auto-reload)
```bash
flask run --debug
```
or
```bash
python app.py
```

Server runs on `http://localhost:5000`

### Production Mode
```bash
flask run
```

### Run Tests
```bash
pytest
```

### View Database Stats
```python
from app import app
from utils.db_seed import DatabaseSeeder

with app.app_context():
    stats = DatabaseSeeder.get_stats()
    print(stats)
```

### Clear Database (WARNING)
```bash
flask clear-db
```

## API Endpoints

### Health Check
- **GET** `/api/health` - Check if server is running

### Search Clubs
- **POST** `/api/search` - Search for clubs based on preferences
  - Request body:
    ```json
    {
      "keywords": "coding",
      "categories": ["Academic", "Music"],
      "availability": ["Monday-Afternoon", "Friday-Evening"]
    }
    ```
  - Response: List of clubs sorted by match score (0-100)

### Get All Clubs
- **GET** `/api/clubs?page=1&per_page=20` - Get paginated list of all clubs

### Get Club Details
- **GET** `/api/clubs/<id>` - Get detailed information about a specific club

## Project Structure

```
backend/
├── app.py                 # Main Flask application & routes
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore file
├── README.md             # This file
├── clubs.db              # SQLite database (created after init-db)
├── sample_clubs.csv      # Sample data in CSV format
├── sample_clubs.json     # Sample data in JSON format
├── models/
│   └── __init__.py       # Club & MeetingTime models
├── routes/               # API route handlers (for future refactoring)
├── utils/
│   ├── search_engine.py  # Club search & matching algorithm
│   └── db_seed.py        # Database seeding utilities
└── tests/
    ├── __init__.py
    └── test_api.py       # API endpoint tests
```

## Database Schema

### Clubs Table
```sql
CREATE TABLE clubs (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  url TEXT,
  description TEXT,
  category TEXT,
  location TEXT,
  contact_email TEXT,
  member_count INTEGER DEFAULT 0,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Meeting Times Table
```sql
CREATE TABLE meeting_times (
  id INTEGER PRIMARY KEY,
  club_id INTEGER NOT NULL FOREIGN KEY,
  day_of_week TEXT NOT NULL,        -- 'Monday', 'Tuesday', etc.
  time_slot TEXT NOT NULL,           -- 'Afternoon', 'Evening', 'Night'
  meeting_description TEXT,
  UNIQUE(club_id, day_of_week, time_slot)
);
```

## Data Import Formats

### CSV Format
```csv
name,url,description,meeting_times,category
Club Name,https://...,Description here,Monday Afternoon;Thursday Evening,Academic
```
- `meeting_times` should be semicolon-separated for multiple times
- Headers must match exactly

### JSON Format
```json
[
  {
    "name": "Club Name",
    "url": "https://...",
    "description": "Description here",
    "category": "Academic",
    "meeting_times": ["Monday Afternoon", "Thursday Evening"]
  }
]
```

## Search Algorithm

Match scores are calculated (0-100) based on:
- **Keyword matching** (40 points): Name matches worth more than description matches
- **Category matching** (40 points): Club category matches user selection
- **Availability matching** (20 points): Club meeting times overlap with user availability

Results are sorted by match score in descending order.

## Environment Variables

Create a `.env` file with:
```
FLASK_ENV=development
PORT=5000
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///clubs.db
CORS_ORIGINS=http://localhost:3000
```

## TODO

- [ ] Add SQLAlchemy relationships and indices optimization
- [ ] Implement authentication/authorization
- [ ] Add comprehensive error handling
- [ ] Add API documentation (Swagger/OpenAPI)
- [ ] Implement rate limiting
- [ ] Add logging
- [ ] Create data migration scripts
- [ ] Add bulk import functionality
- [ ] Implement search result caching

## CORS Configuration

The server is configured to accept requests from `http://localhost:3000` (React frontend). 
Update the `CORS_ORIGINS` environment variable for different environments.

## Development Notes

- Frontend connects to `http://localhost:5000` when running locally
- Database file (`clubs.db`) is in `.gitignore` and not committed to version control
- Mock data automatically created on first run if database is empty
- Use `DatabaseSeeder` class for importing club data from web scraper

## Testing

Run all tests:
```bash
pytest
```

Run specific test:
```bash
pytest tests/test_api.py::test_health_check
```

Run with coverage:
```bash
pytest --cov=.
```

---

**Last updated**: November 2025
**Status**: Database implementation complete, ready for data import

