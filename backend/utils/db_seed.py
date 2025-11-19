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
        'morning': 'Morning',
        'afternoon': 'Afternoon',
        'evening': 'Evening',
        'night': 'Night',
    }

    @staticmethod
    def seed_from_json(json_file):
        """
        Seed database from JSON file
        
        Expected format:
        [
            {
                "name": "Club Name",
                "website_url": "https://...",
                "picture_id": "pic.jpg",
                "summary": "Club description...",
                "categories": "Category Name",
                "meeting_times": ["Monday Morning", "Thursday Afternoon"]
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
        
        Supports two formats:
        1. TerpLink CSV: Name, WebsiteKey, ProfilePicture, Summary, CategoryNames, MeetingTimes
        2. Simple CSV: name, website_url, picture_id, summary, categories, timing
        """
        try:
            import csv as csv_module
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv_module.DictReader(f)
                count = 0
                
                for row in reader:
                    # Handle both CSV formats
                    club_data = {
                        'name': row.get('Name') or row.get('name'),
                        'website_url': row.get('WebsiteKey') or row.get('website_url'),
                        'picture_id': row.get('ProfilePicture') or row.get('picture_id'),
                        'summary': row.get('Summary') or row.get('summary'),
                        'categories': DatabaseSeeder._parse_categories(
                            row.get('CategoryNames') or row.get('categories')
                        ),
                        'meeting_times': DatabaseSeeder._parse_meeting_times(
                            row.get('MeetingTimes') or row.get('timing')
                        )
                    }
                    count += DatabaseSeeder._add_club(club_data)
                
                db.session.commit()
                print(f"✓ Successfully seeded {count} clubs from {csv_file}")
                return count
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error seeding from CSV: {e}")
            import traceback
            traceback.print_exc()
            return 0

    @staticmethod
    def _parse_categories(categories_str):
        """
        Parse categories from various formats
        - List format: "['Category1', 'Category2']"
        - Semicolon format: "Category1;Category2"
        - Comma format: "Category1, Category2"
        Returns comma-separated string
        """
        if not categories_str:
            return ''
        
        cat_str = str(categories_str).strip()
        categories = []
        
        # Handle list format: "['Category1', 'Category2']"
        if cat_str.startswith('[') and cat_str.endswith(']'):
            import ast
            try:
                cat_list = ast.literal_eval(cat_str)
                categories = cat_list if isinstance(cat_list, list) else [cat_str]
            except:
                # If parsing fails, treat as regular string
                categories = [cat_str]
        # Handle semicolon-separated format
        elif ';' in cat_str:
            categories = [c.strip() for c in cat_str.split(';')]
        # Handle comma-separated format
        elif ',' in cat_str:
            categories = [c.strip() for c in cat_str.split(',')]
        # Handle single value
        else:
            categories = [cat_str]
        
        # Filter out empty strings and join with commas
        return ', '.join([c for c in categories if c])

    @staticmethod
    def _parse_meeting_times(meeting_times_str):
        """
        Parse meeting times from various formats
        - List format: "['Monday Evening', 'Tuesday Morning']"
        - Semicolon format: "Monday Evening;Tuesday Morning"
        - Regular string: "Monday Evening, Tuesday Morning"
        """
        if not meeting_times_str:
            return []
        
        meeting_str = str(meeting_times_str).strip()
        times = []
        
        # Handle list format: "['Monday Evening', 'Tuesday Morning']"
        if meeting_str.startswith('[') and meeting_str.endswith(']'):
            import ast
            try:
                times_list = ast.literal_eval(meeting_str)
                times = times_list if isinstance(times_list, list) else [meeting_str]
            except:
                # If parsing fails, treat as regular string
                times = [meeting_str]
        # Handle semicolon-separated format
        elif ';' in meeting_str:
            times = [t.strip() for t in meeting_str.split(';')]
        # Handle comma-separated format
        elif ',' in meeting_str:
            times = [t.strip() for t in meeting_str.split(',')]
        # Handle single value
        else:
            times = [meeting_str]
        
        return [t for t in times if t]  # Filter out empty strings

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
        Add a single club to the database
        
        Returns: 1 if successful, 0 if club already exists
        """
        try:
            name = club_data.get('name')
            website_url = club_data.get('website_url') or club_data.get('url')
            picture_id = club_data.get('picture_id')
            summary = club_data.get('summary') or club_data.get('description', '')
            categories = club_data.get('categories', '')
            
            # Skip if club already exists
            if Club.query.filter_by(name=name).first():
                print(f"⊘ Club '{name}' already exists, skipping")
                return 0
            
            # Create club object
            club = Club(
                name=name,
                website_url=website_url,
                picture_id=picture_id,
                summary=summary,
                categories=categories
            )
            
            db.session.add(club)
            db.session.flush()  # Get the club ID
            
            # Add meeting times
            meeting_times = club_data.get('meeting_times') or club_data.get('timing', [])
            if isinstance(meeting_times, str):
                meeting_times = [meeting_times]
            
            for meeting_str in meeting_times:
                DatabaseSeeder._add_meeting_time(club.id, meeting_str)
            
            print(f"✓ Added club: {name}")
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
        categories = db.session.query(Club.categories, db.func.count(Club.id)).group_by(Club.categories).all()
        
        return {
            'total_clubs': total_clubs,
            'total_meeting_times': total_meeting_times,
            'categories': dict(categories)
        }
