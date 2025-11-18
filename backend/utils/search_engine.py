"""
Search engine utility for matching clubs with user preferences
"""

from models import Club, MeetingTime, db


class ClubSearchEngine:
    """Handles club search and matching logic"""

    @staticmethod
    def search(keywords='', categories=None, availability=None):
        """
        Search for clubs based on user preferences
        
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

        # Start with all clubs
        query = Club.query

        # Filter by keywords (search in name and description)
        if keywords:
            search_term = f'%{keywords.lower()}%'
            query = query.filter(
                db.or_(
                    db.func.lower(Club.name).ilike(search_term),
                    db.func.lower(Club.description).ilike(search_term)
                )
            )

        # Filter by categories
        if categories:
            query = query.filter(Club.category.in_(categories))

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

        return results

    @staticmethod
    def _calculate_match_score(club, keywords, categories, availability):
        """
        Calculate a match score (0-100) based on how well the club matches preferences
        Scoring breakdown:
        - Keyword matching: 40 points (30 for name, 30 for description)
        - Category matching: 40 points (40 if match, 0 if no match)
        - Availability matching: 20 points (proportional based on matches)
        """
        score = 0

        # Keyword matching (40 points max)
        if keywords:
            keywords_lower = keywords.lower()
            name_match = keywords_lower in club.name.lower()
            desc_match = keywords_lower in (club.description or '').lower()
            
            if name_match:
                score += 30  # Strong match in name
            elif desc_match:
                score += 20  # Match in description

        # Category matching (40 points max)
        if categories:
            if club.category in categories:
                score += 40

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
