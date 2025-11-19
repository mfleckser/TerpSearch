import React from 'react';
import './SearchForm.css';

function SearchForm({ formData, setFormData, onSubmit }) {
  const categories = [
    'Science and Technology',
    'Social Fraternity/Sorority',
    'Business and Entrepreneurship',
    'Cultural/Ethnic',
    'Military',
    'Academic and Pre-Professional',
    'Activism/Advocacy/Awareness',
    'Sports and Recreation',
    'Creative and Performing Arts',
    'Academic/College',
    'College - Business (SUSA)',
    'Professional',
    'Health and Wellness',
    'Political',
    'Service',
    'Media/Publications',
    'Religious/Spiritual',
    'E-Sports and Gaming',
    'Honorary/Honor Society',
  ];

  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const timeSlots = ['Morning', 'Afternoon', 'Evening', 'Night'];

  const handleKeywordsChange = (e) => {
    setFormData({ ...formData, keywords: e.target.value });
  };

  const handleCategoryToggle = (category) => {
    setFormData((prev) => ({
      ...prev,
      categories: prev.categories.includes(category)
        ? prev.categories.filter((c) => c !== category)
        : [...prev.categories, category],
    }));
  };

  const handleTimeAvailabilityToggle = (day, timeSlot) => {
    const key = `${day}-${timeSlot}`;
    setFormData((prev) => ({
      ...prev,
      availability: prev.availability.includes(key)
        ? prev.availability.filter((a) => a !== key)
        : [...prev.availability, key],
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
          value={formData.keywords || ''}
          onChange={handleKeywordsChange}
        />
      </div>

      {/* Categories Multi-Select */}
      <div className="form-group">
        <label>Club Categories</label>
        <div className="categories-container">
          {categories.map((category) => (
            <label key={category} className="category-checkbox">
              <input
                type="checkbox"
                checked={formData.categories?.includes(category) || false}
                onChange={() => handleCategoryToggle(category)}
              />
              <span className="category-label">{category}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Time Availability */}
      <div className="form-group">
        <label>Time Availability</label>
        <p className="time-subtitle">Select when you're available to attend meetings</p>
        <div className="availability-grid">
          {daysOfWeek.map((day) => (
            <div key={day} className="day-column">
              <div className="day-header">{day.slice(0, 3)}</div>
              <div className="time-slots">
                {timeSlots.map((timeSlot) => {
                  const key = `${day}-${timeSlot}`;
                  const isSelected = formData.availability?.includes(key) || false;
                  return (
                    <label key={key} className={`time-slot ${isSelected ? 'selected' : ''}`}>
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => handleTimeAvailabilityToggle(day, timeSlot)}
                      />
                      <span className="time-label">{timeSlot.slice(0, 1)}</span>
                    </label>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
        <div className="time-legend">
          <span><strong>M</strong> = Morning</span>
          <span><strong>A</strong> = Afternoon</span>
          <span><strong>E</strong> = Evening</span>
          <span><strong>N</strong> = Night</span>
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
