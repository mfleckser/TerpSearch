"""
Database models for TerpSearch
"""

from flask_sqlalchemy import SQLAlchemy

# Database instance
db = SQLAlchemy()


class Club(db.Model):
    """Club model representing a student organization"""
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True, index=True)
    website_url = db.Column(db.String(512), nullable=False)
    picture_id = db.Column(db.String(255), nullable=True)
    summary = db.Column(db.Text, nullable=False)
    categories = db.Column(db.String(500), nullable=False)  # Comma-separated or JSON string
    summary_embedding = db.Column(db.LargeBinary, nullable=True)  # Stores pre-computed embeddings as binary

    # Relationships
    meeting_times = db.relationship('MeetingTime', backref='club', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert club object to dictionary for JSON responses"""
        return {
            'id': self.id,
            'name': self.name,
            'website_url': self.website_url,
            'picture_id': self.picture_id,
            'summary': self.summary,
            'categories': self.categories,
            'meeting_times': [mt.to_dict() for mt in self.meeting_times]
        }

    def __repr__(self):
        return f'<Club {self.name}>'


class MeetingTime(db.Model):
    """Meeting time model representing when a club meets"""
    __tablename__ = 'meeting_times'

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False, index=True)
    day_of_week = db.Column(db.String(10), nullable=False)  # 'Monday', 'Tuesday', etc.
    time_slot = db.Column(db.String(20), nullable=False)     # 'Morning', 'Afternoon', 'Evening', 'Night'
    meeting_description = db.Column(db.String(255), nullable=True)  # e.g., "Thursdays at 6:00 PM"

    # Unique constraint to prevent duplicate entries
    __table_args__ = (
        db.UniqueConstraint('club_id', 'day_of_week', 'time_slot', name='uq_club_meeting'),
    )

    def to_dict(self):
        """Convert meeting time object to dictionary"""
        return {
            'id': self.id,
            'day_of_week': self.day_of_week,
            'time_slot': self.time_slot,
            'meeting_description': self.meeting_description
        }

    def __repr__(self):
        return f'<MeetingTime {self.club.name} - {self.day_of_week} {self.time_slot}>'
