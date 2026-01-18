import React, { useEffect, useState } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  // Use REACT_APP_API_BASE_URL or fallback to localhost
  const apiBase = process.env.REACT_APP_API_BASE_URL || `http://localhost:8000/api`;
  const endpoint = `${apiBase}/workouts/`;

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setWorkouts(results);
        console.log('Workouts API endpoint:', endpoint);
        console.log('Fetched workouts:', results);
      })
      .catch(err => console.error('Error fetching workouts:', err));
  }, [endpoint]);

  return (
    <div>
      <h2>Workouts</h2>
      <ul>
        {workouts.map((workout, idx) => (
          <li key={workout.id || idx}>{workout.name || JSON.stringify(workout)}</li>
        ))}
      </ul>
    </div>
  );
};

export default Workouts;
