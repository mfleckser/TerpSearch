# TerpSearch - AI Coding Agent Instructions

## Project Overview

**TerpSearch** is a modular search application with three main components:
- **Frontend**: React 19 SPA (Create React App bootstrap)
- **Backend**: Empty/planned (structure exists but no implementation)
- **Scraping**: Empty/planned (structure exists but no implementation)

The project is in early stages with only the frontend framework initialized.

## Architecture & Component Boundaries

### Frontend (`/frontend`)
- **Framework**: React 19 with Create React App (CRA)
- **Entry Point**: `src/index.js` → renders `App` component to `#root` DOM element
- **Main Component**: `App.js` manages page routing and club search state
- **Pages**: `SearchPage` (form) and `ResultsPage` (grid display)
- **Styling**: Component-scoped CSS with `shared.css` for global styles
- **Build System**: CRA's `react-scripts` (v5.0.1)
- **Target Title**: "Terp Search" (visible in browser tab, set in `public/index.html`)

### Backend (`/backend`)
- **Framework**: Flask 3.0.0 with SQLAlchemy 3.0.5 ORM
- **Database**: SQLite (development, file: `clubs.db`), PostgreSQL-ready (production)
- **Entry Point**: `app.py` - runs on `http://localhost:5000`
- **CORS**: Configured to accept requests from `http://localhost:3000` (React frontend)
- **Auto-Categorization**: ClubCategorizer utility automatically assigns categories based on club name and description
- **Key Endpoints**:
  - `GET /api/health` - Health check
  - `GET /api/categories` - Get list of all available club categories
  - `POST /api/search` - Search clubs by keywords, categories, and availability (returns match scores 0-100)
  - `GET /api/clubs` - Get paginated list of all clubs
  - `GET /api/clubs/<id>` - Get detailed club information
- **Structure**:
  - `app.py` - Main Flask application with SQLAlchemy integration, all route implementations, CLI commands
  - `models/__init__.py` - SQLAlchemy models: Club and MeetingTime with relationships
  - `config.py` - Environment-based configuration (Development/Production/Testing)
  - `utils/search_engine.py` - ClubSearchEngine class with matching algorithm
  - `utils/categorizer.py` - ClubCategorizer class for automatic club categorization
  - `utils/db_seed.py` - DatabaseSeeder class supporting CSV/JSON/programmatic data import
  - `tests/` - Unit and integration tests with pytest
- **Dependencies**: Flask, Flask-CORS, Flask-SQLAlchemy 3.0.5, Flask-Migrate, python-dotenv, pytest
- **CLI Commands**:
  - `flask init-db` - Initialize database (create all tables)
  - `flask seed-db` - Populate with 5 sample clubs (auto-categorized)
  - `flask clear-db` - Delete all clubs and reset database
- **Database Models**: 
  - Club (name, url, description, category, meeting_times)
  - MeetingTime (club_id FK, day_of_week, time_slot, meeting_description)
- **Categories**: Academic, Music, Sports, Arts, Cultural, Social, Recreation, Greek Life, Other

### Scraping (`/scraping`)
Currently empty. When implemented:
- Document data sources and scraping targets
- Define data pipeline and storage strategy
- Clarify if it feeds backend database or runs separately

## Critical Developer Workflows

### Frontend Development

**Start development server**:
```bash
cd frontend && npm start
```
- Runs on `http://localhost:3000`
- Hot-reloads on file changes
- Opens browser automatically

**Production build**:
```bash
cd frontend && npm run build
```
- Creates optimized bundle in `frontend/build/`
- Minified with hashed filenames
- Ready for deployment

**Run tests**:
```bash
cd frontend && npm test
```
- Jest-based, runs in watch mode by default
- Uses `@testing-library/react` for component testing

### Backend Development

**First-time setup**:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Initialize database**:
```bash
flask init-db
```

**Seed with sample data**:
```bash
flask seed-db
```

**Start development server** (with auto-reload):
```bash
cd backend && flask run --debug
```
- Runs on `http://localhost:5000`
- Auto-reloads on file changes
- Database queries executed against SQLite or configured database

**Run tests**:
```bash
cd backend && pytest
```
- Unit tests in `tests/` directory
- Tests use in-memory database

**Import clubs from CSV/JSON**:
```python
from app import app
from utils.db_seed import DatabaseSeeder

with app.app_context():
    # From CSV
    DatabaseSeeder.seed_from_csv('sample_clubs.csv')
    # From JSON
    DatabaseSeeder.seed_from_json('sample_clubs.json')
```

**Test specific endpoint**:
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"keywords":"coding","categories":["Academic"],"availability":["Monday-Afternoon"]}'
```

## Code Structure Conventions

### Database Schema (Backend)

**Club Model** (`models/__init__.py`)
```python
class Club(db.Model):
    id: int (primary key)
    name: str (required, unique)
    url: str (required)
    website_url: str (required)
    picture_id: str (optional) - reference to club image
    summary: str (required)
    categories: str (required) - category names (comma-separated if multiple)
    meeting_times: relationship [MeetingTime] - one-to-many
```

**MeetingTime Model** (`models/__init__.py`)
```python
class MeetingTime(db.Model):
    id: int (primary key)
    club_id: int (foreign key to Club.id)
    day_of_week: str (required) - e.g., "Monday", "Tuesday", ..., "Sunday"
    time_slot: str (required) - e.g., "Morning", "Afternoon", "Evening", "Night"
    meeting_description: str (optional) - additional details
    # Unique constraint: (club_id, day_of_week, time_slot) prevents duplicates
```
- See `CATEGORY_GUIDE.md` for how to modify categories

**Search Algorithm** (`utils/search_engine.py`)
- **Match Score (0-100):** 
  - Keyword matching (40 pts): 30 pts for name match, 10 pts for description match
  - Category filter (40 pts): 40 pts if club category matches any requested category
  - Availability overlap (20 pts): Proportional based on availability matches
- **Time Format:** Frontend sends "Monday-Afternoon" → backend parses to day_of_week="Monday", time_slot="Afternoon"
- **Query Logic:** 
  1. Filter clubs by keyword match (ILIKE case-insensitive on name + description)
  2. Filter by selected categories (if any)
  3. Calculate match score for each club
  4. Sort by score descending
  5. Return paginated results with scores attached

**Data Import Formats** (`utils/db_seed.py`)

CSV Format (categories auto-assigned):
```csv
name,url,description,meeting_times
Computer Science Club,https://csclub.umd.edu,Learn to code together,"Monday Afternoon,Wednesday Evening"
```

JSON Format (categories auto-assigned):
```json
[
  {
    "name": "Computer Science Club",
    "url": "https://csclub.umd.edu",
    "description": "Learn to code together",
    "meeting_times": ["Monday Afternoon", "Wednesday Evening"]
  }
]
```

**Meeting Time Parsing:** Converts strings like "Monday Afternoon" to {day_of_week: "Monday", time_slot: "Afternoon"} using pattern matching in db_seed.py

### React Component Patterns
- Use functional components (React 19+)
- Entry point pattern: `src/index.js` mounts root component to DOM element with id 'root'
- CSS modules co-located with components (e.g., `App.js` + `App.css`)
- Form state managed with `useState`; custom hooks for async operations (`useClubSearch`)

### Flask Backend Patterns
- All routes return JSON responses
- CORS enabled for frontend communication
- Mock data in endpoints for development
- TODO comments mark integration points (database, search algorithms)
- Error handlers for common HTTP status codes (404, 500)

### ESLint Configuration
- Extends `react-app` and `react-app/jest` presets (CRA defaults)
- No custom overrides configured yet

### Testing
- **Frontend**: Test library: `@testing-library/react` v16.3.0
- **Backend**: Pytest framework with test fixtures

## Key Dependencies & Versions

| Package | Version | Purpose | Module |
|---------|---------|---------|--------|
| `react` | ^19.2.0 | Core framework | Frontend |
| `react-dom` | ^19.2.0 | DOM rendering | Frontend |
| `react-scripts` | 5.0.1 | CRA build tooling | Frontend |
| `@testing-library/react` | ^16.3.0 | Component testing | Frontend |
| `flask` | 3.0.0 | Web framework | Backend |
| `flask-cors` | 4.0.0 | CORS handling | Backend |
| `python-dotenv` | 1.0.0 | Environment variables | Backend |
| `pytest` | 7.4.0 | Testing framework | Backend |

## Integration Points

- **Frontend ↔ Backend**: Frontend calls `POST /api/search` with query data; backend returns ranked clubs. Base URL configured in `useClubSearch.js` (default: `http://localhost:5000`)
- **Backend ↔ Database**: Not yet implemented. TODO: Add SQLAlchemy models and database schema
- **Frontend ↔ Scraping**: No visible integration yet. Clarify if scraping feeds backend database or runs separately

## Project Setup Instructions

First-time setup:
```bash
# Clone and navigate
cd frontend

# Install dependencies
npm install

# Start development
npm start
```

## Next Steps for New Contributors

1. ✅ Frontend scaffolding complete - search interface and results display implemented
2. ✅ Backend API with database fully implemented - all 5 endpoints functional with SQLAlchemy
3. ✅ Database schema complete - Club and MeetingTime models with relationships
4. ✅ Search algorithm complete - 0-100 scoring based on keyword + category + availability
5. ✅ Data import utilities - CSV, JSON, and programmatic seeding supported
6. ✅ Test suite - 8 comprehensive test cases with proper fixtures
7. ⏳ Next: Web scraping module (use DatabaseSeeder to import data when ready)
8. ⏳ Next: Advanced features (user accounts, favorites, notifications)
9. ⏳ Next: Deployment configuration (Heroku, AWS, Docker)

## Immediate Setup

To get the app running:

1. **Backend setup**:
   ```bash
   cd backend && pip install -r requirements.txt
   flask init-db
   flask seed-db
   flask run --debug
   ```

2. **Frontend setup** (in a new terminal):
   ```bash
   cd frontend && npm install
   npm start
   ```

3. **Run tests**:
   ```bash
   cd backend && pytest tests/test_api.py
   ```

---

**Last updated**: November 2025  
**Status**: Core features complete (frontend, backend, database, search, seeding); ready for scraping integration and advanced features
