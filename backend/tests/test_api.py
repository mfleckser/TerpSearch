"""
Tests for TerpSearch backend API
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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


def test_search_clubs_success(client):
    """Test successful club search"""
    payload = {
        'keywords': 'coding',
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


def test_get_all_clubs(client):
    """Test get all clubs endpoint"""
    response = client.get('/api/clubs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'clubs' in data


def test_get_club_detail(client):
    """Test get club detail endpoint"""
    response = client.get('/api/clubs/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert 'name' in data


def test_not_found(client):
    """Test 404 error handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
