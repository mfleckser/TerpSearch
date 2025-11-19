"""
Script to add summary_embedding column to clubs table if it doesn't exist.
"""

from app import app, db
from models import Club
from sqlalchemy import inspect

def add_embedding_column():
    """Add summary_embedding column to clubs table if it doesn't exist"""
    with app.app_context():
        # Check if column already exists
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('clubs')]
        
        if 'summary_embedding' in columns:
            print("✓ Column 'summary_embedding' already exists")
            return True
        
        # Add the column
        try:
            db.engine.execute('ALTER TABLE clubs ADD COLUMN summary_embedding BLOB')
            print("✓ Added 'summary_embedding' column to clubs table")
            return True
        except Exception as e:
            print(f"✗ Error adding column: {e}")
            # Try alternative syntax for SQLite
            try:
                with db.engine.connect() as conn:
                    conn.execute('ALTER TABLE clubs ADD COLUMN summary_embedding BLOB')
                    conn.commit()
                print("✓ Added 'summary_embedding' column to clubs table")
                return True
            except Exception as e2:
                print(f"✗ Alternative syntax also failed: {e2}")
                return False

if __name__ == '__main__':
    add_embedding_column()
