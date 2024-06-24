import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { getWeatherIcon } from "../weatherIcons"; // Correct path
import "./Weather.css";

const Weather = ({ data }) => {
  // Render a message if no weather data is available
  if (!data) {
    return <div>No weather data available. Please enter a city and date.</div>;
  }

  // Get the appropriate weather icon based on the condition
  const weatherIcon = getWeatherIcon(data.condition);

  return (
    <div className="weather-container">
      {/* Display the city name */}
      <h2>Weather in {data.city}</h2>
      <p className="condition">
        Condition: <span className="condition-icon">{weatherIcon}</span>{" "}
        {data.condition}
      </p>
      {/* Display the date */}
      <p>Date: {data.date}</p>
      {/* Display the average temperature, formatted to 2 decimal places */}
      <p>Temperature: {data.avg_temp.toFixed(2)} °C</p>
      {/* Display the minimum temperature, formatted to 2 decimal places */}
      <p>Min Temperature: {data.min_temp.toFixed(2)} °C</p>
      {/* Display the maximum temperature, formatted to 2 decimal places */}
      <p>Max Temperature: {data.max_temp.toFixed(2)} °C</p>

      {/* Display the minimum humidity */}
      <p>Min Humidity: {data.min_humidity}%</p>
      {/* Display the maximum humidity */}
      <p>Max Humidity: {data.max_humidity}%</p>
      {/* Display the average humidity */}
      <p>Avg Humidity: {data.avg_humidity}%</p>
    </div>
  );
};

export default Weather;
