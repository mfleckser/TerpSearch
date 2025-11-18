"""
Tests for TerpSearch backend API
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db, Club, MeetingTime
from config import TestingConfig


@pytest.fixture
def client():
    """Create a test client with test database"""
    app.config.from_object(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_club(client):
    """Create a sample club for testing"""
    with app.app_context():
        club = Club(
            name='Test Club',
            url='https://example.com/test',
            description='A test club',
            category='Academic'
        )
        db.session.add(club)
        db.session.flush()
        
        # Add meeting times
        mt1 = MeetingTime(club_id=club.id, day_of_week='Monday', time_slot='Afternoon')
        mt2 = MeetingTime(club_id=club.id, day_of_week='Thursday', time_slot='Evening')
        db.session.add_all([mt1, mt2])
        db.session.commit()
        
        return club.id


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_search_clubs_missing_body(client):
    """Test search endpoint with missing request body"""
    response = client.post('/api/search')
    assert response.status_code == 400


def test_search_clubs_success(client, sample_club):
    """Test successful club search"""
    payload = {
        'keywords': 'test',
        'categories': ['Academic'],
        'availability': ['Monday-Afternoon']
    }
    response = client.post('/api/search', 
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'clubs' in data
    assert isinstance(data['clubs'], list)
    if len(data['clubs']) > 0:
        assert 'matchScore' in data['clubs'][0]


def test_search_clubs_empty_result(client):
    """Test search with no matching results"""
    payload = {
        'keywords': 'nonexistent',
        'categories': [],
        'availability': []
    }
    response = client.post('/api/search', 
                          data=json.dumps(payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'clubs' in data
    assert len(data['clubs']) == 0


def test_get_all_clubs(client, sample_club):
    """Test get all clubs endpoint"""
    response = client.get('/api/clubs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'clubs' in data
    assert 'total' in data
    assert 'pages' in data


def test_get_club_detail(client, sample_club):
    """Test get club detail endpoint"""
    response = client.get(f'/api/clubs/{sample_club}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Club'
    assert 'meeting_times' in data


def test_get_club_detail_not_found(client):
    """Test get club detail with invalid ID"""
    response = client.get('/api/clubs/9999')
    assert response.status_code == 404


def test_not_found(client):
    """Test 404 error handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404

