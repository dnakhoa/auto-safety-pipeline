# =============================================================================
# PHASE 1 (RESET): Extraction from Open Food Facts
#
# This script fetches data for a single product from the Open Food Facts
# public API using its barcode and saves the raw data to a JSON file.
# This API requires NO authentication.
# =============================================================================

import requests
import json

# -----------------------------------------------------------------------------
# Step 1: Configuration
# -----------------------------------------------------------------------------
# The barcode of the product we want to look up.
# Example: Arnott's Tim Tam Original
BARCODE = "9310072002778"

# The API is structured simply: base_url/api/version/product/barcode.json
API_ENDPOINT = f"https://world.openfoodfacts.org/api/v2/product/{BARCODE}.json"

OUTPUT_FILENAME = f"product_{BARCODE}.json"

print(f"Fetching data for product with barcode: {BARCODE}")
print(f"API Endpoint: {API_ENDPOINT}")

# -----------------------------------------------------------------------------
# Step 2: API Call and Data Fetching
# -----------------------------------------------------------------------------
print("\nFetching data...")

try:
    # Make the GET request. No headers or keys are needed.
    response = requests.get(API_ENDPOINT, timeout=10)

    # Check if the request was successful.
    response.raise_for_status()

    # Convert the response to a Python dictionary.
    raw_data = response.json()
    print("Successfully fetched product data.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred with the API request: {e}")
    exit()

# -----------------------------------------------------------------------------
# Step 3: Save Raw Data to a Local File
# -----------------------------------------------------------------------------
# Check if the product was found before trying to save.
if raw_data.get("status") == 0:
    print(f"Error: Product with barcode {BARCODE} not found.")
    print(f"Response from server: {raw_data.get('status_verbose')}")
    exit()


print(f"Saving raw data to local file: {OUTPUT_FILENAME}...")

try:
    with open(OUTPUT_FILENAME, 'w') as f:
        # The entire response is valuable, so we save it all.
        json.dump(raw_data, f, indent=4)
    print("Data successfully saved.")

except IOError as e:
    print(f"An error occurred while writing the file: {e}")


# -----------------------------------------------------------------------------
# End of Phase 1 Script
# -----------------------------------------------------------------------------
print("\nPhase 1 (Extraction) complete.")