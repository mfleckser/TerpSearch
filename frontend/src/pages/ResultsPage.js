import React from 'react';
import Header from '../components/Header';
import ClubCard from '../components/ClubCard';

function ResultsPage({ searchQuery, clubs, loading, onBack }) {
  return (
    <div className="results-page">
      <Header />
      
      <div className="results-container">
        <div className="results-header">
          <button className="back-button" onClick={onBack}>
            ← Back to Search
          </button>
          <h1>Search Results</h1>
          {searchQuery && (
            <p className="search-summary">
              Showing results for: <strong>{searchQuery.keywords || 'all clubs'}</strong>
            </p>
          )}
        </div>

        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading clubs...</p>
          </div>
        ) : clubs.length > 0 ? (
          <div className="clubs-grid">
            {clubs.map((club) => (
              <ClubCard key={club.id} club={club} />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No clubs found. Try different search preferences.</p>
            <button className="new-search-button" onClick={onBack}>
              Start New Search
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsPage;
