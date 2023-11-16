import React, { useState } from 'react';
import './Fields.css';

const Fields = () => {
  const [field1, setField1] = useState('');
  const [field2, setField2] = useState('');

  const handleButtonClick = () => {
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
        // Handle success, e.g., update state or show a success message
      })
      .catch(error => {
        console.error('Error sending data', error);
        // Handle error, e.g., show an error message
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
          placeholder="Field 1"
        />
        <input
          type="text"
          value={field2}
          onChange={(e) => setField2(e.target.value)}
          className="input"
          placeholder="Field 2"
        />
      </div>
      <button onClick={handleButtonClick} className="button">
        Send Data
      </button>
    </div>
  );
};

export default Fields;
