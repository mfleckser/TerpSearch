#!/bin/bash
# Setup script to prepare the database with embeddings

echo "🚀 Setting up TerpSearch embeddings..."
echo ""

# Step 1: Add embedding column to database if it doesn't exist
echo "1️⃣ Adding embedding column to database..."
python3 << 'EOF'
from app import app, db
from models import Club
from sqlalchemy import text

with app.app_context():
    try:
        # Try to query the embedding column to see if it exists
        result = db.session.execute(text("SELECT summary_embedding FROM clubs LIMIT 1"))
        print("✓ Column 'summary_embedding' already exists")
    except:
        # Column doesn't exist, add it
        try:
            db.session.execute(text("ALTER TABLE clubs ADD COLUMN summary_embedding BLOB"))
            db.session.commit()
            print("✓ Added 'summary_embedding' column to clubs table")
        except Exception as e:
            print(f"⚠ Could not add column: {e}")
            print("  This is okay if using a fresh database with init-db")

EOF

echo ""
echo "2️⃣ Pre-computing embeddings for all clubs..."
echo "   (This may take 1-2 minutes for 1000+ clubs)"
echo ""

# Step 2: Vectorize all clubs
cd /Users/mfleckser/Documents/College/KTP/TerpSearch/backend
source venv/bin/activate
flask vectorize-clubs

echo ""
echo "✅ Setup complete! Embeddings are now pre-computed and stored."
