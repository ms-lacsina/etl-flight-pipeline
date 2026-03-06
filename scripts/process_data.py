import json

def amending_data(input_path, output_path):
    with open(input_path, "r") as json_file: #Raw string
        data = json.load(json_file) #Load JSON file (list)

    
    #Filtering "terminal" : "T1" and removing "paxProfiles"

    filtered_data = []
    for flight in data: 
        if flight.get("terminal", "").strip().upper() == "T1" and flight.get("flightTypeIATA") in ["C", "J", "G", "O"]:
            flight.pop("paxProfiles", None) #Removing fields here
            flight.pop("destinationICAO", None)
            flight.pop("airlineICAO", None)
            flight.pop("aircraftTypeICAO", None)
            flight.pop("aircraftTypeIATA", None)
            flight.pop("flightTypeICAO", None)
            filtered_data.append(flight)
            if "fields" in flight and isinstance(flight["fields"], list):
                flight["fields"] = [
                    field for field in flight ["fields"]
                    if field.get("name") != "TailRegistration"
                ]


    # Debugging: Show total flights filtered
    print(f"Total flights matching criteria: {len(filtered_data)}")

    #Save new, filtered data back to a new JSON file

    with open(output_path, "w") as output_file:
        json.dump(filtered_data, output_file, indent=4)

if __name__ == "__main__":
    input_path = "data/flight_data.json"
    output_path = "data/filtered_flight_data.json"
    amending_data(input_path, output_path)


import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")# Logging level set to DEBUG

def filter_flights(data):
    logging.debug(f"Original data received: {data}")
    # Apply filtering criteria
    filtered_data = [f for f in data if f['terminal'].strip().upper() == 'T1' and f['flightTypeIATA'] in ['C', 'J', 'G', 'O']]
    if not filtered_data:
        logging.warning("No flights matched criteria.")
    logging.debug(f"Filtered data: {filtered_data}")
    return filtered_data



import requests

# Power BI API credentials
api_url = "https://api.powerbi.com/v1.0/magairports/reports/{report_id}/Refresh"
headers = {"Authorization": "Bearer {access_token}"}

# Trigger Power BI dataset refresh
response = requests.post(api_url, headers=headers)
if response.status_code == 202:
    print("Power BI dataset refresh initiated successfully.")
else:
    print(f"Failed to refresh dataset: {response.status_code}")



