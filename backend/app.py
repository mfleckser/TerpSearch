import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from config import config
from models import db, Club, MeetingTime
from utils.search_engine import ClubSearchEngine

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize database
db.init_app(app)

# Enable CORS for frontend communication
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})




# ==================== ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Backend is running'}), 200


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get list of all available club categories"""
    try:
        from utils.categorizer import ClubCategorizer
        categories = ClubCategorizer.get_category_list()
        return jsonify({'categories': categories}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_clubs():
    """
    Search for clubs based on user preferences
    
    Expected request body:
    {
      "keywords": "string (optional)",
      "categories": ["string"],
      "availability": ["string"] (e.g., ["Monday-Afternoon", "Friday-Evening"])
    }
    
    Returns:
    {
      "clubs": [
        {
          "id": "number",
          "name": "string",
          "category": "string",
          "description": "string",
          "matchScore": "number (0-100)",
          "url": "string",
          "location": "string",
          "meeting_times": [...]
        }
      ]
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        keywords = data.get('keywords', '')
        categories = data.get('categories', [])
        availability = data.get('availability', [])
        
        # Use search engine to find matching clubs
        results = ClubSearchEngine.search(keywords, categories, availability)
        
        # Format response
        clubs_response = []
        for result in results:
            club = result['club']
            club_dict = club.to_dict()
            club_dict['matchScore'] = result['matchScore']
            clubs_response.append(club_dict)
        
        return jsonify({'clubs': clubs_response}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clubs', methods=['GET'])
def get_all_clubs():
    """Get all clubs (with optional pagination)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = ClubSearchEngine.get_all_clubs(page=page, per_page=per_page)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clubs/<int:club_id>', methods=['GET'])
def get_club_detail(club_id):
    """Get detailed information about a specific club"""
    try:
        club = ClubSearchEngine.get_club_by_id(club_id)
        
        if not club:
            return jsonify({'error': 'Club not found'}), 404
        
        return jsonify(club.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ==================== CLI COMMANDS ====================

@app.cli.command()
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("✓ Database initialized")


@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    from utils.db_seed import DatabaseSeeder
    
    with app.app_context():
        # Sample data
        sample_clubs = [
            {
                'name': 'Computer Science Club',
                'url': 'https://example.com/cs-club',
                'description': 'A club for students interested in computer science and programming.',
                'meeting_times': ['Monday Afternoon', 'Thursday Evening']
            },
            {
                'name': 'Outdoor Adventure Club',
                'url': 'https://example.com/outdoor-club',
                'description': 'Join us for hiking, camping, and outdoor activities!',
                'meeting_times': ['Saturday Afternoon']
            },
            {
                'name': 'Entrepreneurship Club',
                'url': 'https://example.com/entrepreneurship',
                'description': 'Learn about starting and growing businesses and startups.',
                'meeting_times': ['Tuesday Evening', 'Friday Afternoon']
            },
            {
                'name': 'Jazz Band',
                'url': 'https://example.com/jazz-band',
                'description': 'Perform jazz music and enjoy improvisation with fellow musicians.',
                'meeting_times': ['Wednesday Evening', 'Saturday Afternoon']
            },
            {
                'name': 'Ultimate Frisbee Club',
                'url': 'https://example.com/ultimate-frisbee',
                'description': 'Competitive and recreational ultimate frisbee sports.',
                'meeting_times': ['Tuesday Afternoon', 'Friday Afternoon']
            }
        ]
        
        DatabaseSeeder.seed_from_data(sample_clubs)
        stats = DatabaseSeeder.get_stats()
        print(f"\nDatabase stats: {stats}")
        
        # Print auto-categorized clubs
        from models import Club
        clubs = Club.query.all()
        print("\nAuto-categorized clubs:")
        for club in clubs:
            print(f"  • {club.name}: {club.category}")


@app.cli.command()
def clear_db():
    """Clear all data from database (WARNING: use with caution)"""
    from utils.db_seed import DatabaseSeeder
    
    with app.app_context():
        confirm = input("⚠ Are you sure you want to clear the database? (yes/no): ")
        if confirm.lower() == 'yes':
            DatabaseSeeder.clear_all()
        else:
            print("✓ Cancelled")
        if confirm.lower() == 'yes':
            DatabaseSeeder.clear_all()
        else:
            print("✓ Cancelled")

# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
