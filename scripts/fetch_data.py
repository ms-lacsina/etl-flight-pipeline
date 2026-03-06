import requests
from datetime import datetime
import json

def fetch_forecast_data():
    # Get today's date in the required format (YYYY-MM-DD)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Define the URL with the formatted date
    url = f'https://betterairport.eu/mag/api/v2/o/447bd96c9499/Forecast/Flights/scheduleFlights/published/{today}?includeShowUpProfiles=True'
    
    headers = {
        'Authorization': 'Basic VXNlcl9TVE5fMDE6eDZxOWNWN2l4VVlJUjZUOG5DMmxLVmRrUVZxZ3RpbmtiNDZSMTVtRg=='
    }
    
    # Sending the GET request to the API
    response = requests.get(url, headers=headers)
    
    # Checking if the response was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        with open("data/flight_data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

            print ("Data saved to flight_data.json")
        
    else:
        print(f"Failed to fetch data: {response.status_code}")


# Calling the function to fetch data
fetch_forecast_data()