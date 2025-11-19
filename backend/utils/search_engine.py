"""
Search engine utility for matching clubs with user preferences
"""

from models import Club, MeetingTime, db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Try to import sentence transformers for semantic embeddings
try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    embedding_model = None


class ClubSearchEngine:
    """Handles club search and matching logic"""

    @staticmethod
    def search(keywords='', categories=None, availability=None):
        """
        Search for clubs based on user preferences using semantic similarity.
        
        The embedding model will automatically find semantically related clubs.
        For example, searching "coding" will return clubs about programming, 
        development, software engineering, etc. without hardcoded mappings.
        
        Args:
            keywords (str): Keywords to search in club name and description
            categories (list): List of categories to filter by
            availability (list): List of availability slots (e.g., ['Monday-Afternoon'])
        
        Returns:
            list: List of Club objects with match scores, sorted by relevance
        """
        if categories is None:
            categories = []
        if availability is None:
            availability = []

        # Get all clubs (we'll score them all semantically)
        query = Club.query

        # Filter by categories if provided (categories field is comma-separated)
        if categories:
            category_filters = []
            for category in categories:
                category_filters.append(
                    db.func.lower(Club.categories).contains(db.func.lower(category))
                )
            query = query.filter(db.or_(*category_filters))

        clubs = query.all()

        # Calculate match scores and filter by availability
        results = []
        for club in clubs:
            match_score = ClubSearchEngine._calculate_match_score(
                club, keywords, categories, availability
            )
            
            # Include club if availability matches or if no availability filter
            if not availability or ClubSearchEngine._check_availability_match(club, availability):
                results.append({
                    'club': club,
                    'matchScore': match_score
                })

        # Sort by match score (highest first)
        results.sort(key=lambda x: x['matchScore'], reverse=True)

        # Limit to top 30 results
        return results[:30]

    @staticmethod
    def _calculate_match_score(club, keywords, categories, availability):
        """
        Calculate a match score (0-100) based on how well the club matches preferences.
        Uses embedding-based semantic similarity with pre-computed embeddings when available.
        
        Scoring breakdown:
        - Keyword matching: 40 points (25 for name/keywords overlap, 15 for semantic similarity)
        - Category matching: 40 points (40 if match, 0 if no match)
        - Availability matching: 20 points (proportional based on matches)
        """
        score = 0
        keywords_lower = keywords.lower() if keywords else ''

        # Keyword matching (40 points max)
        if keywords:
            # Check for keyword in club name (25 points)
            if keywords_lower in club.name.lower():
                score += 25
            
            # Semantic similarity to summary (15 points max)
            # Pass the pre-computed embedding for faster similarity calculation
            if club.summary:
                similarity_score = ClubSearchEngine._calculate_semantic_similarity(
                    keywords, 
                    club.summary,
                    club_embedding_bytes=club.summary_embedding  # Use pre-stored embedding
                )
                # Convert 0-100 similarity to 0-15 points
                score += int((similarity_score / 100) * 15)

        # Category matching (40 points max)
        # categories field is comma-separated, check if any requested category is in the club's categories
        if categories:
            club_categories_lower = club.categories.lower() if club.categories else ''
            for category in categories:
                if category.lower() in club_categories_lower:
                    score += 40
                    break  # Only count once even if multiple categories match

        # Availability matching (20 points max)
        if availability:
            availability_match_count = 0
            for slot in availability:
                if ClubSearchEngine._has_meeting_slot(club, slot):
                    availability_match_count += 1
            
            if availability_match_count > 0:
                # Award points based on percentage of availability matches
                score += int(20 * (availability_match_count / len(availability)))

        # Normalize to 0-100 range
        return min(100, max(0, score))

    @staticmethod
    def _calculate_semantic_similarity(keywords, club_summary, club_embedding_bytes=None):
        """
        Calculate semantic similarity using pre-computed embeddings or on-the-fly computation.
        
        For best performance, club_embedding_bytes should be provided (pre-stored embedding).
        If not provided, falls back to computing embedding or TF-IDF similarity.
        
        Args:
            keywords (str): User's search keywords
            club_summary (str): Club's summary text
            club_embedding_bytes (bytes): Pre-computed embedding stored as binary
        
        Returns:
            int: Similarity score (0-100)
        """
        if not keywords or not club_summary:
            return 0
        
        try:
            if SENTENCE_TRANSFORMERS_AVAILABLE and embedding_model is not None:
                # Encode the query
                query_embedding = embedding_model.encode(keywords, convert_to_tensor=True)
                
                # Use pre-computed embedding if available
                if club_embedding_bytes is not None:
                    # Convert bytes back to numpy array, then to tensor
                    club_embedding_np = np.frombuffer(club_embedding_bytes, dtype=np.float32)
                    club_embedding = embedding_model._first_module().tokenizer.encode(club_summary)  # Temporary fallback
                    # Actually just use the stored embedding directly
                    try:
                        import torch
                        club_embedding = torch.from_numpy(club_embedding_np).to(query_embedding.device)
                    except:
                        # Fallback: compute on the fly
                        club_embedding = embedding_model.encode(club_summary, convert_to_tensor=True)
                else:
                    # Compute embedding on the fly if not stored
                    club_embedding = embedding_model.encode(club_summary, convert_to_tensor=True)
                
                # Calculate cosine similarity
                similarity = util.pytorch_cos_sim(query_embedding, club_embedding)
                similarity_score = float(similarity)
                
                # Convert to 0-100 score
                return int(similarity_score * 100)
            else:
                # Fallback to TF-IDF if sentence-transformers not available
                minimal_stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'are', 'am', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
                
                vectorizer = TfidfVectorizer(
                    lowercase=True,
                    stop_words=list(minimal_stop_words),
                    ngram_range=(1, 2),
                    max_features=200,
                    min_df=1
                )
                
                texts = [keywords, club_summary]
                tfidf_matrix = vectorizer.fit_transform(texts)
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                
                return int(similarity * 100)
        except Exception as e:
            # Fallback: simple substring matching on error
            if keywords.lower() in club_summary.lower():
                return 50
            return 0

    @staticmethod
    def _check_availability_match(club, availability_slots):
        """Check if club has at least one meeting matching user's availability"""
        for slot in availability_slots:
            if ClubSearchEngine._has_meeting_slot(club, slot):
                return True
        return False

    @staticmethod
    def _has_meeting_slot(club, slot):
        """Check if club has a meeting in the given slot (e.g., 'Monday-Afternoon')"""
        try:
            day, time = slot.split('-')
            return MeetingTime.query.filter_by(
                club_id=club.id,
                day_of_week=day,
                time_slot=time
            ).first() is not None
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def get_all_clubs(page=1, per_page=20):
        """Get paginated list of all clubs"""
        paginated = Club.query.paginate(page=page, per_page=per_page)
        return {
            'clubs': [club.to_dict() for club in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }

    @staticmethod
    def get_club_by_id(club_id):
        """Get a specific club by ID"""
        return Club.query.get(club_id)
