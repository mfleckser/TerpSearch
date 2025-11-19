"""
Automatic club categorization based on name and description
Uses keyword matching and pattern recognition
"""


class ClubCategorizer:
    """Categorize clubs based on keywords in name and description"""
    
    # Define category keywords (customize as needed)
    CATEGORY_KEYWORDS = {
        'Science and Technology': [
            'coding', 'programming', 'computer', 'science', 'engineering', 'tech',
            'technology', 'software', 'hardware', 'ai', 'machine learning', 'data',
            'robotics', 'research', 'physics', 'chemistry', 'biology', 'stem'
        ],
        'Social Fraternity/Sorority': [
            'fraternity', 'sorority', 'greek', 'frat', 'brotherhood', 'sisterhood',
            'pledge', 'greek life', 'social fraternity', 'social sorority'
        ],
        'Business and Entrepreneurship': [
            'business', 'entrepreneurship', 'startup', 'consulting', 'consulting',
            'economics', 'finance', 'accounting', 'marketing', 'sales', 'case competition',
            'investment', 'trading', 'venture'
        ],
        'Cultural/Ethnic': [
            'cultural', 'international', 'language', 'spanish', 'chinese', 'arabic',
            'french', 'german', 'korean', 'japanese', 'indian', 'african', 'heritage',
            'community', 'ethnic', 'diaspora', 'asia', 'latin', 'caribbean', 'cultural'
        ],
        'Military': [
            'military', 'rotc', 'army', 'navy', 'air force', 'marine', 'veteran',
            'armed forces', 'defense'
        ],
        'Academic and Pre-Professional': [
            'debate', 'argumentation', 'public speaking', 'mock trial', 'model un',
            'prelaw', 'pre-law', 'pre-med', 'premed', 'pre-dental', 'predental',
            'academic competition', 'scholarship'
        ],
        'Activism/Advocacy/Awareness': [
            'activism', 'advocacy', 'awareness', 'social justice', 'environment',
            'sustainability', 'sustainability', 'climate', 'conservation', 'volunteer',
            'volunteering', 'charity', 'outreach', 'community service', 'mental health'
        ],
        'Sports and Recreation': [
            'sports', 'soccer', 'basketball', 'football', 'tennis', 'baseball',
            'volleyball', 'lacrosse', 'crew', 'rowing', 'swimming', 'rugby',
            'frisbee', 'ultimate', 'athletic', 'fitness', 'yoga', 'martial arts',
            'track', 'wrestling', 'golf', 'climbing', 'skateboard', 'snowboard',
            'hiking', 'camping', 'outdoor', 'adventure', 'recreation', 'bike',
            'running', 'cycling', 'dance'
        ],
        'Creative and Performing Arts': [
            'art', 'drawing', 'painting', 'sculpture', 'design', 'photography',
            'film', 'theater', 'drama', 'dance', 'visual', 'creative', 'animation',
            'graphic', 'crafts', 'pottery', 'performance', 'music', 'band', 'orchestra',
            'jazz', 'choir', 'singing', 'instrument', 'musician', 'acoustic', 'electric',
            'vocal', 'symphony', 'rock', 'pop', 'classical'
        ],
        'Academic/College': [
            'academic', 'college', 'engineering', 'nursing', 'agriculture', 'architecture'
        ],
        'College - Business (SUSA)': [
            'business school', 'mba', 'accounting', 'finance', 'management', 'commerce'
        ],
        'Professional': [
            'professional', 'career', 'networking', 'conference', 'mentor', 'mentorship',
            'professional development', 'alumni'
        ],
        'Health and Wellness': [
            'health', 'wellness', 'fitness', 'medical', 'nursing', 'psychology',
            'mental health', 'counseling', 'therapy', 'nutrition', 'exercise',
            'meditation', 'mindfulness', 'yoga'
        ],
        'Political': [
            'political', 'politics', 'campaign', 'government', 'policy', 'congress',
            'senate', 'democrats', 'republicans', 'conservative', 'liberal', 'independent'
        ],
        'Service': [
            'service', 'volunteer', 'community', 'outreach', 'charity', 'humanitarian',
            'relief', 'food bank', 'tutoring', 'mentoring'
        ],
        'Media/Publications': [
            'media', 'publication', 'journalism', 'newspaper', 'magazine', 'yearbook',
            'podcast', 'broadcast', 'radio', 'television', 'tv', 'film', 'video',
            'photography', 'news', 'editor', 'writer', 'reporter'
        ],
        'Religious/Spiritual': [
            'religious', 'spiritual', 'faith', 'church', 'synagogue', 'mosque',
            'temple', 'christian', 'catholic', 'jewish', 'muslim', 'hindu', 'buddhist',
            'interfaith', 'chaplain', 'ministry', 'worship', 'prayer', 'bible', 'quran'
        ],
        'E-Sports and Gaming': [
            'esports', 'gaming', 'video games', 'game', 'competitive gaming', 'tournament',
            'twitch', 'streaming', 'discord', 'league of legends', 'valorant', 'overwatch',
            'minecraft', 'dota', 'fortnite', 'gaming'
        ],
        'Honorary/Honor Society': [
            'honor', 'honorary', 'honor society', 'honors', 'prestigious', 'excellence',
            'scholarship', 'academic honors'
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
        return list(ClubCategorizer.CATEGORY_KEYWORDS.keys())
