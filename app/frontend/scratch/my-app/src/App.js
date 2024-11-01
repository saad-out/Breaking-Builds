import React, { useState } from 'react';
import './App.css';
import StageCards from './StageCards';
import data from './data.json'; // Importing the dummy data
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [showStages, setShowStages] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleButtonClick = () => {
    setLoading(true);
    setShowStages(true);
  };

  return (
    <div className="container">
      <h1 className="title">Breaking Builds</h1>
      <p className="description">Realtime Full CI/CD Pipeline with Jenkins</p>
      <button className={loading ? "button-disabled" : "trigger-button" } onClick={handleButtonClick} disabled={loading}>
        { loading ? 'Triggering...' : 'Trigger Build' }
      </button>
      {showStages && <StageCards stages={data} />}
    </div>
  );
}

export default App;

