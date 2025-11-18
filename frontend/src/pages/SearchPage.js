import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';
import Header from '../components/Header';

function SearchPage({ onSearch }) {
  const [formData, setFormData] = useState({
    keywords: '',
    categories: [],
    availability: [],
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Pass form data to parent component
    onSearch(formData);
  };

  return (
    <div className="search-page">
      <Header />
      <div className="search-container">
        <h1>Find Your Club at UMD</h1>
        <p className="subtitle">Discover clubs that match your interests</p>
        <SearchForm 
          formData={formData} 
          setFormData={setFormData} 
          onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
}

export default SearchPage;
