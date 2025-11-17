import React from 'react';

function ClubCard({ club }) {
  return (
    <div className="club-card">
      <div className="card-header">
        <h3>{club.name}</h3>
        {club.category && (
          <span className="category-badge">{club.category}</span>
        )}
      </div>

      {club.matchScore && (
        <div className="match-score">
          <span className="score-label">Match:</span>
          <span className="score-value">{club.matchScore}%</span>
        </div>
      )}

      <p className="description">{club.description}</p>

      {club.meetingTime && (
        <div className="club-info">
          <p><strong>Meeting Time:</strong> {club.meetingTime}</p>
        </div>
      )}

      {club.location && (
        <div className="club-info">
          <p><strong>Location:</strong> {club.location}</p>
        </div>
      )}

      <div className="card-footer">
        <button className="learn-more-button">Learn More</button>
      </div>
    </div>
  );
}

export default ClubCard;
