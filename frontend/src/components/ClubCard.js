import React from 'react';

function ClubCard({ club }) {
  const handleLearnMore = () => {
    if (club.website_url) {
      window.open(`https://terplink.umd.edu/organization/${club.website_url}`, '_blank');
    }
  };

  return (
    <div className="club-card">
      {club.picture_id && (
        <div className="card-image">
          <img 
            src={`https://se-images.campuslabs.com/clink/images/${club.picture_id}`} 
            alt={club.name}
            style={{ width: '100%', height: '200px', objectFit: 'cover' }}
          />
        </div>
      )}

      <div className="card-header">
        <h3>{club.name}</h3>
        {club.categories && (
          <span className="category-badge">{club.categories.split(',')[0].trim()}</span>
        )}
      </div>

      <p className="description">{club.summary}</p>

      <div className="card-footer">
        <button className="learn-more-button" onClick={handleLearnMore}>
          Learn More
        </button>
      </div>
    </div>
  );
}

export default ClubCard;
