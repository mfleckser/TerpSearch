import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Configuration
app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'


# ==================== ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Backend is running'}), 200


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
          "meetingTime": "string",
          "location": "string"
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
        
        # TODO: Implement actual search logic
        # 1. Query database for clubs matching criteria
        # 2. Filter by keywords, categories, and availability
        # 3. Calculate match scores
        # 4. Sort and return results
        
        # Mock data for development
        mock_results = {
            'clubs': [
                {
                    'id': 1,
                    'name': 'Computer Science Club',
                    'category': 'Academic',
                    'description': 'A club for students interested in computer science and programming.',
                    'matchScore': 95,
                    'meetingTime': 'Thursdays at 6:00 PM',
                    'location': 'McKeldin Library'
                },
                {
                    'id': 2,
                    'name': 'Outdoor Adventure Club',
                    'category': 'Recreation',
                    'description': 'Join us for hiking, camping, and outdoor activities!',
                    'matchScore': 87,
                    'meetingTime': 'Saturdays at 10:00 AM',
                    'location': 'McKeldin Library Quad'
                },
                {
                    'id': 3,
                    'name': 'Entrepreneurship Club',
                    'category': 'Academic',
                    'description': 'Learn about starting and growing businesses.',
                    'matchScore': 82,
                    'meetingTime': 'Tuesdays at 7:00 PM',
                    'location': 'Business Building'
                }
            ]
        }
        
        return jsonify(mock_results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clubs', methods=['GET'])
def get_all_clubs():
    """Get all clubs (with optional pagination)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # TODO: Implement pagination and database query
        
        mock_clubs = {
            'clubs': [],
            'total': 0,
            'page': page,
            'per_page': per_page
        }
        
        return jsonify(mock_clubs), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clubs/<int:club_id>', methods=['GET'])
def get_club_detail(club_id):
    """Get detailed information about a specific club"""
    try:
        # TODO: Query database for club details
        
        mock_club = {
            'id': club_id,
            'name': 'Sample Club',
            'category': 'Academic',
            'description': 'Club description here',
            'meetingTime': 'Tuesday at 6:00 PM',
            'location': 'Sample Location',
            'contact': 'email@umd.edu',
            'memberCount': 25
        }
        
        return jsonify(mock_club), 200
        
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


# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
