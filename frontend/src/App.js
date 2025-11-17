
import React, { useState } from 'react';
import './App.css';
import SearchPage from './pages/SearchPage';
import ResultsPage from './pages/ResultsPage';
import { useClubSearch } from './hooks/useClubSearch';

function App() {
  const [currentPage, setCurrentPage] = useState('search'); // 'search' or 'results'
  const [searchQuery, setSearchQuery] = useState(null);
  const { clubs, loading, error, search } = useClubSearch();

  const handleSearch = async (query) => {
    setSearchQuery(query);
    // Call the useClubSearch hook to fetch clubs
    await search(query);
    setCurrentPage('results');
  };

  const handleBackToSearch = () => {
    setCurrentPage('search');
    setSearchQuery(null);
  };

  return (
    <div className="App">
      {currentPage === 'search' ? (
        <SearchPage onSearch={handleSearch} />
      ) : (
        <ResultsPage 
          searchQuery={searchQuery} 
          clubs={clubs} 
          loading={loading}
          onBack={handleBackToSearch}
        />
      )}
    </div>
  );
}

export default App;
