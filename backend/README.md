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
  - Response: List of clubs with match scores

### Get All Clubs
- **GET** `/api/clubs?page=1&per_page=20` - Get paginated list of all clubs

### Get Club Details
- **GET** `/api/clubs/<id>` - Get detailed information about a specific club

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore file
├── README.md             # This file
├── models/               # Database models (to be implemented)
├── routes/               # API route handlers (to be implemented)
├── utils/                # Utility functions (to be implemented)
└── tests/                # Test files (to be implemented)
```

## TODO

- [ ] Implement database connection (SQLAlchemy)
- [ ] Create club data models
- [ ] Implement search algorithm with matching logic
- [ ] Add authentication/authorization
- [ ] Add comprehensive error handling
- [ ] Write unit tests
- [ ] Add API documentation (Swagger/OpenAPI)
- [ ] Implement rate limiting
- [ ] Add logging

## CORS Configuration

The server is configured to accept requests from `http://localhost:3000` (React frontend). 
Update `app.py` line 13 for different environments.

## Environment Variables

Create a `.env` file with:
```
FLASK_ENV=development
PORT=5000
DATABASE_URL=your_database_url_here
```

## Development Notes

- Frontend connects to `http://localhost:5000` when running locally
- Update `.frontend/src/hooks/useClubSearch.js` to point to correct backend URL
- CORS is enabled for frontend communication

---

**Last updated**: November 2025
