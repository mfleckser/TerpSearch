"""
Database seeding utility for populating clubs data
Supports CSV, JSON, and direct data input
"""

import json
import csv
from pathlib import Path
from models import Club, MeetingTime, db
from utils.categorizer import ClubCategorizer


class DatabaseSeeder:
    """Handles database seeding from various data sources"""

    # Mapping of meeting time strings to day/time slots
    # This will need to be customized based on actual scraping format
    MEETING_PATTERNS = {
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday',
    }

    TIME_SLOT_PATTERNS = {
        'afternoon': 'Afternoon',
        'evening': 'Evening',
        'night': 'Night',
        'morning': 'Afternoon',  # Map morning to afternoon for now
    }

    @staticmethod
    def seed_from_json(json_file):
        """
        Seed database from JSON file
        
        Expected format:
        [
            {
                "name": "Club Name",
                "url": "https://...",
                "description": "...",
                "meeting_times": ["Monday Afternoon", "Thursday Evening"],
                "category": "Academic"  # Optional
            }
        ]
        """
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            count = 0
            for club_data in data:
                count += DatabaseSeeder._add_club(club_data)
            
            db.session.commit()
            print(f"✓ Successfully seeded {count} clubs from {json_file}")
            return count
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error seeding from JSON: {e}")
            return 0

    @staticmethod
    def seed_from_csv(csv_file):
        """
        Seed database from CSV file
        
        Expected columns:
        name, url, description, meeting_times, category
        (meeting_times should be semicolon-separated for multiple times)
        """
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                
                for row in reader:
                    club_data = {
                        'name': row.get('name'),
                        'url': row.get('url'),
                        'description': row.get('description'),
                        'meeting_times': row.get('meeting_times', '').split(';') if row.get('meeting_times') else [],
                        'category': row.get('category')
                    }
                    count += DatabaseSeeder._add_club(club_data)
                
                db.session.commit()
                print(f"✓ Successfully seeded {count} clubs from {csv_file}")
                return count
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error seeding from CSV: {e}")
            return 0

    @staticmethod
    def seed_from_data(clubs_data):
        """
        Seed database from Python list of dictionaries
        
        Args:
            clubs_data: List of club dictionaries
        """
        try:
            count = 0
            for club_data in clubs_data:
                count += DatabaseSeeder._add_club(club_data)
            
            db.session.commit()
            print(f"✓ Successfully seeded {count} clubs")
            return count
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error seeding from data: {e}")
            return 0

    @staticmethod
    def _add_club(club_data):
        """
        Add a single club to the database with auto-categorization
        
        Returns: 1 if successful, 0 if club already exists
        """
        try:
            name = club_data.get('name')
            url = club_data.get('url')
            description = club_data.get('description')
            
            # Skip if club already exists
            if Club.query.filter_by(name=name).first():
                print(f"⊘ Club '{name}' already exists, skipping")
                return 0
            
            # Auto-categorize the club based on name and description
            category = club_data.get('category') or ClubCategorizer.categorize(name, description)
            
            # Create club object
            club = Club(
                name=name,
                url=url,
                description=description,
                category=category
            )
            
            db.session.add(club)
            db.session.flush()  # Get the club ID
            
            # Add meeting times
            meeting_times = club_data.get('meeting_times', [])
            if isinstance(meeting_times, str):
                meeting_times = [meeting_times]
            
            for meeting_str in meeting_times:
                DatabaseSeeder._add_meeting_time(club.id, meeting_str)
            
            print(f"✓ Added club: {name} ({category})")
            return 1
        except Exception as e:
            print(f"✗ Error adding club: {e}")
            return 0

    @staticmethod
    def _add_meeting_time(club_id, meeting_str):
        """
        Parse meeting time string and add to database
        
        Attempts to extract day and time slot from string like:
        "Monday Afternoon", "Thursday 6pm", etc.
        """
        try:
            meeting_lower = meeting_str.lower().strip()
            day_found = None
            time_slot_found = None

            # Try to find day of week
            for day_pattern, day_name in DatabaseSeeder.MEETING_PATTERNS.items():
                if day_pattern in meeting_lower:
                    day_found = day_name
                    break

            # Try to find time slot
            for time_pattern, time_name in DatabaseSeeder.TIME_SLOT_PATTERNS.items():
                if time_pattern in meeting_lower:
                    time_slot_found = time_name
                    break

            # Add meeting time if both day and slot found
            if day_found and time_slot_found:
                meeting_time = MeetingTime(
                    club_id=club_id,
                    day_of_week=day_found,
                    time_slot=time_slot_found,
                    meeting_description=meeting_str
                )
                db.session.add(meeting_time)
            else:
                print(f"  ⊘ Could not parse meeting time: '{meeting_str}'")
        except Exception as e:
            print(f"  ✗ Error adding meeting time: {e}")

    @staticmethod
    def clear_all():
        """Clear all clubs from database (use with caution)"""
        try:
            Club.query.delete()
            db.session.commit()
            print("✓ Database cleared")
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error clearing database: {e}")

    @staticmethod
    def get_stats():
        """Get database statistics"""
        total_clubs = Club.query.count()
        total_meeting_times = MeetingTime.query.count()
        categories = db.session.query(Club.category, db.func.count(Club.id)).group_by(Club.category).all()
        
        return {
            'total_clubs': total_clubs,
            'total_meeting_times': total_meeting_times,
            'categories': dict(categories)
        }
