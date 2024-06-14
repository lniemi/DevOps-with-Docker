import React from 'react';
import axios from 'axios';

const BBGRefresher = () => {
  const handleRefresh = () => {
    // Retrieve CSRF token from cookies
    const csrftoken = document.cookie.split('; ')
                           .find(row => row.startsWith('csrftoken='))
                           ?.split('=')[1]; // Added optional chaining for safety

    axios({
      method: 'post',
      url: 'http://localhost:8000/api/fetch_and_upload_bbg_data/', // Full URL including the correct port
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,  // Using the csrftoken variable correctly
      },
    })
    .then(response => {
      alert('Data successfully updated!');
    })
    .catch(error => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        alert(`Failed to update data: ${error.response.data.message}`);
      } else if (error.request) {
        // The request was made but no reaction was received
        alert('Failed to update data: No response from server');
      } else {
        // Something happened in setting up the request that triggered an Error
        alert('Error', error.message);
      }
    });
  };

  return (
    <button onClick={handleRefresh}>Refresh BBG Data</button>
  );
};

export  default BBGRefresher;
