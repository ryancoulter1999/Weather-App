import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the backend app directory to the system path to allow importing the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import the FastAPI app from the main module
from backend.app.main import app

# Create a TestClient instance to simulate requests to the FastAPI app
client = TestClient(app)

# Test case for valid weather data retrieval
def test_get_weather():
    # Send a GET request to the weather endpoint with valid parameters
    response = client.get("/api/weather?city=London&date=2024-06-25")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the response JSON data
    data = response.json()
    
    # Assert that the city in the response is "London"
    assert data["city"] == "London"
    
    # Assert that the date in the response is "2024-06-25"
    assert data["date"] == "2024-06-25"
    
    # Assert that the response contains the expected keys for temperature and humidity
    assert "min_temp" in data
    assert "max_temp" in data
    assert "avg_temp" in data
    assert "min_humidity" in data
    assert "max_humidity" in data
    assert "avg_humidity" in data

# Test case for handling invalid date format
def test_invalid_date_format():
    # Send a GET request to the weather endpoint with an invalid date format
    response = client.get("/api/weather?city=London&date=25-06-2024")
    
    # Assert that the response status code is 400 (Bad Request)
    assert response.status_code == 400

# Test case for handling scenario where no data is found for the specified city and date
def test_no_data_found():
    # Send a GET request to the weather endpoint with a non-existent city
    response = client.get("/api/weather?city=InvalidCity&date=2024-06-25")
    
    # Assert that the response status code is 404 (Not Found)
    assert response.status_code == 404
