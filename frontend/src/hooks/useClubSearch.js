import React, { useState, useCallback } from 'react';

/**
 * Custom hook for handling club search API calls
 * 
 * @param {string} apiBaseUrl - Base URL for the backend API
 * @returns {Object} - { clubs, loading, error, search }
 */
export const useClubSearch = (apiBaseUrl = 'http://127.0.0.1:5000') => {
  const [clubs, setClubs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = useCallback(async (query) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(query),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setClubs(data.clubs || []);
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
