import React, { useState } from 'react';
import './Fields.css';

const Fields = () => {
  const [field1, setField1] = useState('');
  const [field2, setField2] = useState('');
  const [loading, setLoading] = useState(false); // New state for loading indicator
  const [resultLabel, setResultLabel] = useState(null);

  const handleButtonClick = () => {
    setLoading(true); // Set loading state to true when the button is clicked

    // Assuming your Django backend is running on http://localhost:8000
    const apiUrl = 'http://localhost:8000/django_app/handle_frontend_data/';

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        field1,
        field2,
      }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Data sent successfully', data);
        // Extract the score from the response data
        const score = data.score;

        // Format the score as a percentage with 2 decimal places
        const formattedScore = (score * 100).toFixed(2) + '%';

        // Set the formatted score as the resultLabel
        setResultLabel(`Similarity: ${formattedScore}`);

      })
      .catch(error => {
        console.error('Error sending data', error);
        // Handle error, e.g., show an error message
      })
      .finally(() => {
        setLoading(false); // Set loading state back to false after processing
      });
  };

  return (
    <div className="container">
      <div className="input-container">
        <input
          type="text"
          value={field1}
          onChange={(e) => setField1(e.target.value)}
          className="input"
          placeholder="Playlist 1"
        />
        <input
          type="text"
          value={field2}
          onChange={(e) => setField2(e.target.value)}
          className="input"
          placeholder="Playlist 2"
        />
      </div>
      {loading ? (
        <button className="button" disabled>
          Loading...
        </button>
      ) : (
        <button onClick={handleButtonClick} className="button">
          Compare
        </button>
      )}
      {resultLabel && (
      <div className="result-box">
        <p className="result-label">{resultLabel}</p>
      </div>
    )}
    </div>
  );
};

export default Fields;
