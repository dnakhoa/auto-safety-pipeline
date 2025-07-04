# =============================================================================
# PHASE 1: EXTRACTION
#
# This script fetches vehicle recall data from the National Highway Traffic
# Safety Administration (NHTSA) API for a specified date range and saves
# the raw response to a local JSON file.
# =============================================================================

# -----------------------------------------------------------------------------
# Step 1: Import necessary libraries
# -----------------------------------------------------------------------------
import requests  # For making HTTP requests to the API
from datetime import datetime, timedelta  # For handling dates
import json  # For working with JSON data
import os  # To interact with the operating system (e.g., file paths)

# -----------------------------------------------------------------------------
# Step 2: Configuration
# Define the parameters for the API call.
# -----------------------------------------------------------------------------
print("Configuring date range and API endpoint...")

# Calculate the date range: from three years ago to today.
today = datetime.now()
three_years_ago = today - timedelta(days=3 * 365)

# Format the dates into the 'YYYY-MM-DD' string format required by the API.
today_str = today.strftime('%Y-%m-%d')
start_date_str = three_years_ago.strftime('%Y-%m-%d')

# Construct the final API URL using an f-string for easy formatting.
# This is the 'recallsByDateRange' endpoint, which is the most efficient for our goal.
API_ENDPOINT = f"https://api.nhtsa.gov/recalls/recallsByDateRange?fromDate={start_date_str}&toDate={today_str}"

# Define the output filename.
# This ensures each file has a unique name based on when the script was run.
OUTPUT_FILENAME = f"nhtsa_recalls_{today.strftime('%Y_%m_%d')}.json"

print(f"Data will be fetched for the period: {start_date_str} to {today_str}")
print(f"Output will be saved to: {OUTPUT_FILENAME}")

# -----------------------------------------------------------------------------
# Step 3: API Call and Data Fetching
# Make the request to the API and handle potential errors.
# -----------------------------------------------------------------------------
print("\nFetching data from NHTSA API...")

try:
    # Make the GET request to the API endpoint.
    response = requests.get(API_ENDPOINT, timeout=30)  # Set a 30-second timeout

    # Check if the request was successful (i.e., status code 200).
    # If not, this will raise an HTTPError, which is caught by the except block.
    response.raise_for_status()

    # Convert the JSON response text into a Python dictionary.
    raw_data = response.json()
    print(f"Successfully fetched {raw_data.get('Count', 'N/A')} recall campaigns.")

except requests.exceptions.RequestException as e:
    # This block catches any network-related errors (e.g., DNS failure, refused connection).
    print(f"An error occurred with the API request: {e}")
    # Exit the script if we cannot fetch the data, as the rest of the script cannot run.
    exit()

# -----------------------------------------------------------------------------
# Step 4: (Optional) Print a Sample for Confirmation
# This helps you verify that you have received the data you expect.
# -----------------------------------------------------------------------------
# To view the sample, simply uncomment the following lines (remove the #).

# print("\n--- Sample of Raw Data ---")
# # The actual list of recalls is under the 'results' key in the response.
# if 'results' in raw_data and len(raw_data['results']) > 0:
#     # Print the first recall campaign from the list.
#     # We use json.dumps for "pretty-printing" to make it readable.
#     first_recall = raw_data['results'][0]
#     print(json.dumps(first_recall, indent=4))
# else:
#     print("No recall data found in the response.")
# print("--- End of Sample ---\n")


# -----------------------------------------------------------------------------
# Step 5: Save Raw Data to a Local File
# Save the 'results' portion of the data to the specified JSON file.
# -----------------------------------------------------------------------------
print(f"Saving raw data to local file: {OUTPUT_FILENAME}...")

try:
    # We use 'with open' as it safely handles opening and closing the file.
    # 'w' stands for write mode, which will create the file or overwrite it if it exists.
    with open(OUTPUT_FILENAME, 'w') as f:
        # We only want to save the list of recalls, not the metadata like 'Count'.
        # The json.dump() function writes the Python object to the file in JSON format.
        json.dump(raw_data['results'], f, indent=4)
    
    print("Data successfully saved.")
    
except KeyError:
    print("Error: The 'results' key was not found in the API response. Cannot save file.")
except IOError as e:
    print(f"An error occurred while writing the file: {e}")

# -----------------------------------------------------------------------------
# End of Phase 1 Script
# -----------------------------------------------------------------------------
print("\nPhase 1 (Extraction) complete.")