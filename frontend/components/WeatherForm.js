import React, { useState } from "react";

const WeatherForm = ({ onSearch }) => {
  // State variables to store city, date, and error messages
  const [city, setCity] = useState("");
  const [date, setDate] = useState("");
  const [error, setError] = useState("");

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate city name
    if (!isValidCity(city)) {
      setError("Invalid city name. Please enter a valid city.");
      return;
    }
    // Validate date format
    if (!isValidDate(date)) {
      setError("Invalid date format. Please use YYYY-MM-DD.");
      return;
    }
    // Clear error and trigger the search callback
    setError("");
    onSearch(city, date);
  };

  // Function to validate city name
  const isValidCity = (city) => {
    const cityRegex = /^[a-zA-Z\s]+$/;
    return cityRegex.test(city);
  };

  // Function to validate date format
  const isValidDate = (date) => {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    return dateRegex.test(date);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Display error message if any */}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>
        <label>City:</label>
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Date (YYYY-MM-DD):</label>
        <input
          type="text"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
          placeholder="YYYY-MM-DD"
        />
      </div>
      <button type="submit">Get Weather</button>
    </form>
  );
};

export default WeatherForm;
