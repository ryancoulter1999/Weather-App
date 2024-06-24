import logging  # Import the logging module to enable logging functionality

from fastapi import FastAPI  # Import the FastAPI framework for building APIs
from backend.app.weather import router as weather_router  # Import the weather router from a specific module

# Configure logging to display info level messages
logging.basicConfig(level=logging.INFO)

# Initialize the FastAPI application
app = FastAPI()

#Initializes a FastAPI application instance named app. 
# This instance will serve as the main container for defining API endpoints, middleware, dependencies, and other configurations.


# Include the weather router with a specified prefix
app.include_router(weather_router, prefix="/api")

#prefix="/api" specifies that all endpoints defined within weather_router will be prefixed with /api. 
# For example, if weather_router defines an endpoint /weather, it will be accessible at /api/weather.

# Define a root endpoint that returns a welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to the Weather API"}

#The code sets up a FastAPI application (app), configures logging to display INFO level messages, 
# includes a router (weather_router) for handling weather-related API endpoints under the /api prefix, and defines a root endpoint (/) that returns a welcome message when accessed. 
# This structure organizes and initializes the application, defines routing for specific functionality (weather), and provides a basic endpoint (/) for initial interaction with the API.
