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
- **Framework**: Flask 3.0.0 with Python 3.8+
- **Entry Point**: `app.py` - runs on `http://localhost:5000`
- **CORS**: Configured to accept requests from `http://localhost:3000` (React frontend)
- **Key Endpoints**:
  - `POST /api/search` - Search clubs by keywords, categories, and availability
  - `GET /api/clubs` - Get paginated list of all clubs
  - `GET /api/clubs/<id>` - Get detailed club information
  - `GET /api/health` - Health check
- **Structure**:
  - `app.py` - Main Flask application with route definitions
  - `models/` - Database models (to be implemented with SQLAlchemy)
  - `routes/` - Route handlers (to be refactored from app.py)
  - `utils/` - Search matching and utility functions
  - `tests/` - Unit and integration tests
- **Dependencies**: Flask, Flask-CORS, python-dotenv, pytest

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

**Start development server** (with auto-reload):
```bash
cd backend && flask run --debug
```
- Runs on `http://localhost:5000`
- Auto-reloads on file changes

**Run tests**:
```bash
cd backend && pytest
```
- Unit tests in `tests/` directory
- Currently includes API endpoint tests

**Test specific endpoint**:
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"keywords":"coding","categories":["Academic"],"availability":["Monday-Afternoon"]}'
```

## Code Structure Conventions

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

1. **Expand App.js**: Build initial feature (search interface, results display, etc.)
2. **Add styles**: Populate `App.css` or introduce component-level CSS
3. **Implement backend**: Define tech stack and API contract
4. **Implement scraping**: Define data sources and pipeline
5. **Document patterns**: Update this file as new conventions emerge

---

**Last updated**: November 2025  
**Status**: Framework initialized, feature development in progress
