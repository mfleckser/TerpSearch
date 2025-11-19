"""
Utility for pre-computing and storing embeddings for club summaries.
This speeds up search by avoiding on-the-fly embedding computation.
"""

import numpy as np
from models import Club, db
from sentence_transformers import SentenceTransformer

# Initialize embedding model
try:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    MODEL_AVAILABLE = True
except ImportError:
    MODEL_AVAILABLE = False
    embedding_model = None


def vectorize_all_clubs(app):
    """
    Pre-compute embeddings for all club summaries and store in database.
    
    Args:
        app: Flask application instance with app context
    
    Returns:
        dict: Statistics about vectorization (clubs processed, errors, etc.)
    """
    if not MODEL_AVAILABLE:
        return {
            'status': 'error',
            'message': 'Sentence transformers not available'
        }
    
    with app.app_context():
        clubs = Club.query.all()
        total_clubs = len(clubs)
        vectorized_count = 0
        error_count = 0
        
        print(f"Starting vectorization of {total_clubs} clubs...")
        
        for i, club in enumerate(clubs, 1):
            try:
                # Encode the summary to embedding
                embedding = embedding_model.encode(club.summary, convert_to_tensor=False)
                
                # Convert numpy array to bytes for storage
                embedding_bytes = embedding.astype(np.float32).tobytes()
                
                # Store embedding in database
                club.summary_embedding = embedding_bytes
                vectorized_count += 1
                
                if i % 100 == 0:
                    print(f"  Processed {i}/{total_clubs} clubs...")
                
            except Exception as e:
                print(f"  Error vectorizing club '{club.name}': {str(e)}")
                error_count += 1
        
        # Commit all changes
        db.session.commit()
        print(f"Vectorization complete!")
        
        return {
            'status': 'success',
            'total_clubs': total_clubs,
            'vectorized': vectorized_count,
            'errors': error_count,
            'message': f'Successfully vectorized {vectorized_count}/{total_clubs} clubs'
        }


def get_embedding_from_bytes(embedding_bytes):
    """
    Convert stored embedding bytes back to numpy array.
    
    Args:
        embedding_bytes: Binary embedding data from database
    
    Returns:
        numpy.ndarray: Embedding vector
    """
    if embedding_bytes is None:
        return None
    return np.frombuffer(embedding_bytes, dtype=np.float32)


def embedding_to_bytes(embedding):
    """
    Convert embedding array to bytes for storage.
    
    Args:
        embedding: numpy array or tensor
    
    Returns:
        bytes: Binary representation of embedding
    """
    if isinstance(embedding, np.ndarray):
        return embedding.astype(np.float32).tobytes()
    # Handle tensor case
    return embedding.cpu().numpy().astype(np.float32).tobytes()
