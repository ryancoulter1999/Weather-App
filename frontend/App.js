import React, { useState } from "react";
import axios from "axios";
import WeatherForm from "./components/WeatherForm";
import Weather from "./components/Weather";
import { getWeatherIcon } from "./weatherIcons";
import "./App.css";

const App = () => {
  // State to store weather data and error messages
  const [weatherData, setWeatherData] = useState(null);
  const [error, setError] = useState("");

  // Function to fetch weather data from the API
  const fetchWeather = async (city, date) => {
    try {
      // Make a GET request to the weather API
      const response = await axios.get(`/api/weather`, {
        params: { city, date },
      });
      console.log("API Response:", response.data); // Log the API response
      setWeatherData(response.data); // Update state with the fetched weather data
      setError(""); // Clear any previous errors
    } catch (error) {
      console.error("API Error:", error); // Log the API error
      // Set error message based on the response
      if (error.response && error.response.data && error.response.data.detail) {
        setError(error.response.data.detail);
      } else {
        setError("An error occurred while fetching the weather data.");
      }
      setWeatherData(null); // Clear weather data in case of error
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Weather App</h1>
        <div className="weather-icon">
          {/* Display weather icon based on weather data */}
          {weatherData ? getWeatherIcon(weatherData.condition) : "🌤️"}
        </div>
      </header>
      <main>
        {/* Render the WeatherForm component and pass the fetchWeather function as a prop */}
        <WeatherForm onSearch={fetchWeather} />
        {/* Display error message if any */}
        {error && <p className="error-message">{error}</p>}
        {/* Render the Weather component and pass the weather data as a prop */}
        <Weather data={weatherData} />
      </main>
      <footer>
        <p>Weather App &copy; 2024</p>
      </footer>
    </div>
  );
};

export default App;
