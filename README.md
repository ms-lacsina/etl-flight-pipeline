# Flight Forecast ETL Pipeline

## Overview
This repository contains a fully automated ETL pipeline designed to extract, clean, transform, and export daily flight forecast data from the Copenhagen Optimization API. The pipeline prepares operational flight data for analytics, reporting, and forecasting use cases within an airport environment.

The workflow is modular, production‑oriented, and scheduled to run automatically using GitHub Actions.

---

## Objectives
- Automate the retrieval of daily flight forecast data.
- Clean and filter raw JSON into a structured, analytics‑ready format.
- Flatten nested fields and derive additional operational features.
- Export the final dataset as a CSV for consumption by BI tools or modelling workflows.
- Provide a reproducible, maintainable, and extensible ETL architecture.

---

## Architecture
        +---------------------------+
        |  Copenhagen Optimization  |
        |        API (JSON)         |
        +-------------+-------------+
                      |
                      v
            [ Extract Stage ]
            fetch_data.py
                      |
                      v
        Raw JSON → data/flight_data.json
                      |
                      v
            [ Transform Stage 1 ]
            process_data.py
    - Filter Terminal T1 flights Note: London Stansted Airport only has 1 Terminal.
    - Remove unused fields
    - Clean nested structures
                      |
                      v
  Filtered JSON → data/filtered_flight_data.json
                      |
                      v
            [ Transform Stage 2 ]
            transform_data.py
    - Flatten fields
    - Extract schedule date/time
    - Add derived flags
    - Aggregate metrics
                      |
                      v
   Final CSV → data/transformed_flight_data.csv
                      |
                      v
            [ Automation Layer ]
            GitHub Actions (main.yml)


---

## Repository Structure
etl-flight-pipeline/
├── scripts/
    ├── main.py               # Orchestrates the ETL pipeline   
    ├── fetch_data.py         # Extracts raw data from API   
    ├── process_data.py       # Cleans and filters JSON  
    └── transform_data.py     # Flattens and exports CSV  
├── .github/   
└── workflows/      
    └── main.yml          # Scheduled automation workflow
├── data/                     # Raw, filtered, and transformed outputs 
├── logs/                     # Local log files
├── requirements.txt 
└── README.md

---

## Components

### **1. `scripts/main.py`**
Coordinates the ETL workflow:
- Sets up logging
- Defines file paths
- Executes extract → clean → transform sequence
- Handles exceptions and logs errors

### **2. `scripts/fetch_data.py`**
- Calls the Copenhagen Optimization API using a daily timestamp
- Saves the raw JSON response to `data/flight_data.json`
- Includes authentication header and request validation

### **3. `scripts/process_data.py`**
- Filters flights to Terminal **T1**
- Removes unused fields (e.g., ICAO codes, paxProfiles)
- Cleans nested `fields` list (e.g., removes TailRegistration)
- Outputs `filtered_flight_data.json`

### **4. `scripts/transform_data.py`**
- Flattens nested JSON into a tabular structure
- Extracts schedule date and time components
- Adds derived operational flags:
  - `HasWarnings`
  - `LowLoadFactor`
  - `HighLoadFactor`
- Computes aggregates:
  - Totals by destination
  - Totals by EU status
  - Totals by CTA status
- Exports final CSV to `data/transformed_flight_data.csv`

---

## Automation (GitHub Actions)

The workflow located at `.github/workflows/main.yml`:

- Runs daily at **07:00 GMT** and **07:00 BST**
- Installs dependencies
- Ensures required folders exist
- Executes the ETL pipeline end‑to‑end

This enables the pipeline to operate without manual intervention.

---

## How to Run Locally

1. Create a virtual environment
```bash
python -m venv venv

2. Activate the environment
Windows:
venv\Scripts\activate


Mac/Linux:
source venv/bin/activate


3. Install dependencies
pip install -r requirements.txt


4. Run the pipeline
python scripts/main.py



Output Files
|  |  | 
| data/flight_data.json |  | 
| data/filtered_flight_data.json |  | 
| data/transformed_flight_data.csv |  | 



Skills Demonstrated
- API integration and authentication
- JSON parsing and nested data handling
- Data cleaning and transformation
- Feature engineering
- Logging and error handling
- Automation with GitHub Actions
- Modular, production‑ready Python design
- Reproducible ETL architecture


Author
Maria Sophia Lacsina

