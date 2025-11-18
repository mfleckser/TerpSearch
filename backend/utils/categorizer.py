"""
Automatic club categorization based on name and description
Uses keyword matching and pattern recognition
"""


class ClubCategorizer:
    """Categorize clubs based on keywords in name and description"""
    
    # Define category keywords (customize as needed)
    CATEGORY_KEYWORDS = {
        'Academic': [
            'coding', 'programming', 'computer', 'science', 'engineering', 'math',
            'physics', 'chemistry', 'biology', 'business', 'economics', 'research',
            'debate', 'case competition', 'consulting', 'entrepreneurship', 'startup',
            'analytics', 'data', 'statistics'
        ],
        'Music': [
            'music', 'band', 'orchestra', 'jazz', 'choir', 'singing', 'instrument',
            'performance', 'musician', 'acoustic', 'electric', 'vocal', 'symphony',
            'rock', 'pop', 'classical'
        ],
        'Sports': [
            'sports', 'soccer', 'basketball', 'football', 'tennis', 'baseball',
            'volleyball', 'lacrosse', 'crew', 'rowing', 'swimming', 'rugby',
            'frisbee', 'ultimate', 'athletic', 'fitness', 'yoga', 'martial arts',
            'track', 'wrestling', 'golf', 'climbing'
        ],
        'Arts': [
            'art', 'drawing', 'painting', 'sculpture', 'design', 'photography',
            'film', 'theater', 'drama', 'dance', 'visual', 'creative', 'animation',
            'graphic', 'crafts', 'pottery', 'performance'
        ],
        'Cultural': [
            'cultural', 'international', 'language', 'spanish', 'chinese', 'arabic',
            'french', 'german', 'korean', 'japanese', 'indian', 'african', 'heritage',
            'community', 'ethnic', 'diaspora', 'asia', 'latin', 'caribbean'
        ],
        'Social': [
            'social', 'community service', 'volunteering', 'volunteer', 'charity',
            'social justice', 'activism', 'environment', 'sustainability', 'outreach',
            'mentoring', 'support group', 'network', 'professional'
        ],
        'Recreation': [
            'outdoor', 'adventure', 'hiking', 'camping', 'climbing', 'kayaking',
            'board games', 'tabletop', 'gaming', 'rpg', 'recreation', 'hobby',
            'travel', 'exploration', 'adventure', 'nature'
        ],
        'Greek Life': [
            'fraternity', 'sorority', 'greek', 'frat', 'brotherhood',
            'sisterhood', 'pledge', 'greek life'
        ]
    }
    
    @staticmethod
    def categorize(club_name, club_description):
        """
        Automatically categorize a club based on name and description
        
        Args:
            club_name (str): The club name
            club_description (str): The club description
            
        Returns:
            str: The predicted category name
        """
        # Combine name and description for keyword matching
        text = f"{club_name} {club_description}".lower()
        
        # Score each category based on keyword matches
        category_scores = {}
        for category, keywords in ClubCategorizer.CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        # Return category with highest score, default to 'Other'
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        else:
            return 'Other'
    
    @staticmethod
    def get_category_list():
        """Return all available categories"""
        return list(ClubCategorizer.CATEGORY_KEYWORDS.keys()) + ['Other']
