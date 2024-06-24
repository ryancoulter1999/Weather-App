from fastapi import FastAPI, APIRouter, HTTPException, Query  # Importing necessary FastAPI components
from pydantic import BaseModel  # Importing BaseModel for defining response models
from datetime import datetime, timedelta  # Importing datetime and timedelta for date manipulation
import requests  # Library for making HTTP requests
import statistics  # Library for statistical operations
import os  # Library for interacting with the operating system
import logging  # Python's built-in logging module

# Initialize the FastAPI application instance named 'app'
app = FastAPI()

# Configure logging to display info level messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a new API router creates a new router instance 
# named router specifically for defining API endpoints related to weather.
router = APIRouter()

# Define the response model for weather data
class WeatherResponse(BaseModel):
    city: str
    date: str
    min_temp: float
    max_temp: float
    avg_temp: float
    min_humidity: float
    max_humidity: float
    avg_humidity: float
    condition: str
    #WeatherResponse is a Pydantic model (BaseModel) that defines the structure of the 
    # response expected from the /api/weather endpoint. 
    # It includes fields such as 
    # city, date, min_temp, max_temp, avg_temp, min_humidity, max_humidity, avg_humidity, and condition, 
    # each with its expected data type.


    # ENDPOINT DEFINITION: - Define an endpoint to get weather data 
@router.get("/api/weather", response_model=WeatherResponse)


#PARAMETER VALIDATION: - Specifies  that 'city' is a required string parameter, ensuring it meets the min 2 character and matches the regex pattern
async def get_weather(city: str = Query(..., min_length=1, regex="^[a-zA-Z\s]+$"), date: str = Query(...)):

    # Retrieve the API key from environment variables
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured.")
    
    try:
        # Parse and validate the target date
        target_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Expected format: YYYY-MM-DD")
    

# DATE PARSING:

#target_date = datetime.strptime(date, "%Y-%m-%d") attempts to parse the date parameter into a datetime object, 
# expecting the format YYYY-MM-DD. If parsing fails (ValueError), an HTTPException with a status code of 400 is raised, indicating a bad request due to an invalid date format.

    try:
        # Calculate the timestamp range for the target date
        start_date = int(target_date.timestamp())
        end_date = int((target_date + timedelta(days=1)).timestamp())
        #Date Range Calculation: Together, start_date and end_date define a timestamp range that spans exactly 24 hours from target_date to the next day. 
        # This range is used to filter and retrieve weather data specifically for the target_date from an external API (like OpenWeatherMap).

        # Construct the API URL for fetching weather data
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(url) # makes a GET request to the constructed URL.
        response.raise_for_status() #checks for any HTTP errors in the response; if there are any, it raises an exception.

        # Parse the API response
        data = response.json()
        logger.info(f"API Response: {data}")

        temps = [] #Initializes empty lists to store weather data
        humidities = []
        conditions = []

        # Extract temperature, humidity, and weather condition data for the target date
        for item in data['list']:
            if start_date <= item['dt'] < end_date:
                temps.append(item['main']['temp'])
                humidities.append(item['main']['humidity'])
                if 'weather' in item and len(item['weather']) > 0:
                    conditions.append(item['weather'][0]['main'])
                    #Iterates through data['list'] (forecast items from the API response), extracting 
                    # temp, humidity, and weather condition if they fall within the specified start_date and end_date

        logger.info(f"Extracted conditions: {conditions}")
        #Logs the extracted conditions.

        if not temps or not humidities or not conditions:
            raise HTTPException(status_code=404, detail="No data found for the specified date.")
        #Raises an HTTPException with status code 404 if no data (temps, humidities, or conditions lists are empty) is found for the specified date.

    
        # DATA ANALYSIS AND RESPONSE CONSTRUCTION:
        condition = statistics.mode(conditions) #Uses statistics.mode(conditions) to determine the most common weather condition for the day.
        logger.info(f"Selected condition: {condition}") #Logs the selected Condition

        # Construct the weather response
        weather_response = WeatherResponse(
            city=city,
            date=date,
            min_temp=min(temps),
            max_temp=max(temps),
            avg_temp=statistics.mean(temps),
            min_humidity=min(humidities),
            max_humidity=max(humidities),
            avg_humidity=statistics.mean(humidities),
            condition=condition
        )
        #Constructs a WeatherResponse object using the extracted data (city, date, temps, humidities, and condition).
        
        logger.info(f"WeatherResponse: {weather_response}") #Logs the constructed 'Weather Response'
        
        return weather_response #Returns weather_response, which will be serialized to JSON and returned as the API response.

    #ERROR HANDLING:    
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors from the API request
        logger.error(f"HTTP error: {http_err}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found.")
        else:
            raise HTTPException(status_code=500, detail=str(http_err)) #Logs the HTTP error and raises an appropriate HTTPException depending on the status code 
                                                                       #(404 for "City not found" or 500 for other HTTP errors).
        
    except Exception as e:
        # Handle general exceptions
        logger.error(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 
    #Catches general exceptions (Exception) to handle any other unexpected errors, 
    #logs the error, and raises an HTTPException with status code 500.

    # Include the weather router in the FastAPI application
    app.include_router(router)

    #In summary, app.include_router(router) is used in FastAPI to combine separate routing modules (router) into the main application (app), 
    #effectively extending the application's functionality and organizing endpoints logically.



    
    



    




