import React, { useState, useCallback } from 'react';

/**
 * Custom hook for handling club search API calls
 * 
 * @param {string} apiBaseUrl - Base URL for the backend API
 * @returns {Object} - { clubs, loading, error, search }
 */
export const useClubSearch = (apiBaseUrl = 'http://localhost:5000') => {
  const [clubs, setClubs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = useCallback(async (query) => {
    setLoading(true);
    setError(null);
    try {
      // TODO: Replace with actual backend API call
      // const response = await fetch(`${apiBaseUrl}/api/search`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(query),
      // });
      // 
      // if (!response.ok) {
      //   throw new Error(`API error: ${response.status}`);
      // }
      // 
      // const data = await response.json();
      // setClubs(data.clubs || []);

      // Mock data for demonstration
      const mockClubs = [
        {
          id: 1,
          name: 'Computer Science Club',
          category: 'Academic',
          description: 'A club for students interested in computer science and programming.',
          matchScore: 95,
          meetingTime: 'Thursdays at 6:00 PM',
          location: 'McKeldin Library',
        },
        {
          id: 2,
          name: 'Outdoor Adventure Club',
          category: 'Recreation',
          description: 'Join us for hiking, camping, and outdoor activities!',
          matchScore: 87,
          meetingTime: 'Saturdays at 10:00 AM',
          location: 'McKeldin Library Quad',
        },
      ];

      setClubs(mockClubs);
    } catch (err) {
      setError(err.message || 'Failed to fetch clubs');
      setClubs([]);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl]);

  return { clubs, loading, error, search };
};

export default useClubSearch;
