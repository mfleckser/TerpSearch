#!/usr/bin/env python3
"""
Quick setup script for TerpSearch backend
Run this after cloning to set up the database quickly
"""

import os
import sys

def main():
    print("🚀 TerpSearch Backend Setup\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Check if venv exists
    venv_path = 'venv'
    if not os.path.exists(venv_path):
        print("⚠️  Virtual environment not found")
        print("   Run: python3 -m venv venv")
        print("   Then: source venv/bin/activate")
        sys.exit(1)
    
    print("✓ Virtual environment found")
    
    # Check if Flask is installed
    try:
        import flask
        print("✓ Flask installed")
    except ImportError:
        print("❌ Flask not installed. Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Initialize app context
    from app import app, db
    from utils.db_seed import DatabaseSeeder
    
    with app.app_context():
        print("\n📁 Database Setup")
        
        # Create tables
        print("  → Creating database tables...")
        db.create_all()
        print("  ✓ Tables created")
        
        # Check if database has data
        from models import Club
        club_count = Club.query.count()
        
        if club_count == 0:
            print("\n📊 Seeding with sample data...")
            
            # Sample data
            sample_clubs = [
                {
                    'name': 'Computer Science Club',
                    'url': 'https://example.com/cs-club',
                    'description': 'A club for students interested in computer science and programming.',
                    'category': 'Academic',
                    'meeting_times': ['Monday Afternoon', 'Thursday Evening']
                },
                {
                    'name': 'Outdoor Adventure Club',
                    'url': 'https://example.com/outdoor-club',
                    'description': 'Join us for hiking, camping, and outdoor activities!',
                    'category': 'Recreation',
                    'meeting_times': ['Saturday Afternoon']
                },
                {
                    'name': 'Entrepreneurship Club',
                    'url': 'https://example.com/entrepreneurship',
                    'description': 'Learn about starting and growing businesses.',
                    'category': 'Academic',
                    'meeting_times': ['Tuesday Evening', 'Friday Afternoon']
                },
                {
                    'name': 'Jazz Band',
                    'url': 'https://example.com/jazz-band',
                    'description': 'Perform jazz music and enjoy improvisation.',
                    'category': 'Music',
                    'meeting_times': ['Wednesday Evening', 'Saturday Afternoon']
                },
                {
                    'name': 'Ultimate Frisbee Club',
                    'url': 'https://example.com/ultimate-frisbee',
                    'description': 'Competitive and recreational ultimate frisbee.',
                    'category': 'Sports',
                    'meeting_times': ['Tuesday Afternoon', 'Friday Afternoon']
                }
            ]
            
            DatabaseSeeder.seed_from_data(sample_clubs)
            
            # Get stats
            stats = DatabaseSeeder.get_stats()
            print(f"\n  📈 Database Stats:")
            print(f"     Total Clubs: {stats['total_clubs']}")
            print(f"     Total Meeting Times: {stats['total_meeting_times']}")
            print(f"     Categories: {dict(stats['categories'])}")
        else:
            print(f"\n  ℹ️  Database already contains {club_count} clubs")
        
        print("\n✅ Setup complete!")
        print("\n🏃 To start the server, run:")
        print("   flask run --debug")
        print("\n📚 For more info, see README.md")


if __name__ == '__main__':
    main()
