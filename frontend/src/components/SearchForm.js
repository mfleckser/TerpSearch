import React from 'react';

function SearchForm({ formData, setFormData, onSubmit }) {
  const categories = [
    'All Categories',
    'Music',
    'Sports',
    'Academic',
    'Social',
    'Greek Life',
    'Service',
    'Cultural',
    'Religious',
  ];

  const interestOptions = [
    'Leadership',
    'Community Service',
    'Competitive',
    'Casual',
    'Networking',
    'Recreation',
    'Arts',
    'STEM',
  ];

  const handleKeywordsChange = (e) => {
    setFormData({ ...formData, keywords: e.target.value });
  };

  const handleCategoryChange = (e) => {
    setFormData({ ...formData, category: e.target.value });
  };

  const handleInterestsToggle = (interest) => {
    setFormData((prev) => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter((i) => i !== interest)
        : [...prev.interests, interest],
    }));
  };

  return (
    <form className="search-form" onSubmit={onSubmit}>
      {/* Keywords Input */}
      <div className="form-group">
        <label htmlFor="keywords">Search Keywords</label>
        <input
          type="text"
          id="keywords"
          placeholder="e.g., coding, dance, environmental..."
          value={formData.keywords}
          onChange={handleKeywordsChange}
        />
      </div>

      {/* Category Dropdown */}
      <div className="form-group">
        <label htmlFor="category">Category</label>
        <select
          id="category"
          value={formData.category}
          onChange={handleCategoryChange}
        >
          {categories.map((cat) => (
            <option key={cat} value={cat === 'All Categories' ? '' : cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {/* Interests Multi-Select */}
      <div className="form-group">
        <label>Interests</label>
        <div className="interests-container">
          {interestOptions.map((interest) => (
            <label key={interest} className="interest-checkbox">
              <input
                type="checkbox"
                checked={formData.interests.includes(interest)}
                onChange={() => handleInterestsToggle(interest)}
              />
              <span className="interest-label">{interest}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Submit Button */}
      <button type="submit" className="search-button">
        Find Clubs
      </button>
    </form>
  );
}

export default SearchForm;
