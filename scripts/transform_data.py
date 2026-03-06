import json
import csv
from datetime import datetime

def transform_data(input_path, output_csv_path):
    # Load the filtered JSON data
    with open(input_path, "r") as json_file:
        data = json.load(json_file)

    # Prepare the transformed data list
    transformed_data = []

    # Initialise aggregates for debugging/logging
    totals_by_destination = {}
    totals_by_eu_status = {}
    totals_by_cta_status = {}

    for flight in data:
        # Convert scheduleTime to date and time components
        try:
            original_schedule = flight.get("scheduleTime", "")
            converted_schedule = datetime.fromisoformat(original_schedule.replace("Z", ""))
            schedule_date = converted_schedule.strftime("%Y-%m-%d")
            schedule_hour = converted_schedule.strftime("%H:%M:%S")
        except ValueError:
            schedule_date = None
            schedule_hour = None

        # Flatten fields for easy CSV export
        flat_flight = {
            "airlineIATA": flight.get("airlineIATA"),
            "destinationIATA": flight.get("destinationIATA"),
            "flightNumber": flight.get("flightNumber"),
            "flightNature": flight.get("flightNature"),
            "flightTypeIATA": flight.get("flightTypeIATA"),
            "scheduleDate": schedule_date,
            "scheduleHour": schedule_hour,
            "seatCapacity": flight.get("seatCapacity"),
            "sector": flight.get("sector"),
            "terminal": flight.get("terminal"),
            "pax": flight.get("pax", 0),
            "loadFactor": flight.get("loadFactor", 0),
            "warnings": "; ".join(flight.get("warnings", [])),  # Combine warnings into a single string
        }

        # Extract "fields" into the flat dictionary
        for field in flight.get("fields", []):
            flat_flight[field["name"]] = field["value"]

        # Add derived fields
        flat_flight["HasWarnings"] = bool(flight.get("warnings"))
        flat_flight["LowLoadFactor"] = flat_flight["loadFactor"] <= 0.1
        flat_flight["HighLoadFactor"] = flat_flight["loadFactor"] > 1.0

        # Update aggregates
        totals_by_destination[flat_flight["destinationIATA"]] = (
            totals_by_destination.get(flat_flight["destinationIATA"], 0) + flat_flight["pax"]
        )
        totals_by_eu_status[flat_flight.get("EU Status", "Unknown")] = (
            totals_by_eu_status.get(flat_flight.get("EU Status", "Unknown"), 0) + flat_flight["pax"]
        )
        totals_by_cta_status[flat_flight.get("CTA Status", "Unknown")] = (
            totals_by_cta_status.get(flat_flight.get("CTA Status", "Unknown"), 0) + flat_flight["pax"]
        )

        # Add to the list of transformed data
        transformed_data.append(flat_flight)

    # Write the transformed data to a CSV file
    with open(output_csv_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=transformed_data[0].keys())
        writer.writeheader()
        writer.writerows(transformed_data)

    # Debugging: Print aggregates
    print("Totals by Destination:")
    for destination, total in totals_by_destination.items():
        print(f"  {destination}: {total}")

    print("\nTotals by EU Status:")
    for status, total in totals_by_eu_status.items():
        print(f"  {status}: {total}")

    print("\nTotals by CTA Status:")
    for status, total in totals_by_cta_status.items():
        print(f"  {status}: {total}")


if __name__ == "__main__":
    input_path = "data/filtered_flight_data.json"
    output_csv_path = "data/transformed_flight_data.csv"
    transform_data(input_path, output_csv_path)
