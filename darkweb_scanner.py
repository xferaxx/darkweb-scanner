import requests  # Import the requests library for making HTTP requests
import time  # Import the time library to add delays between requests
import os  # Import the os library to access environment variables
import json  # Import the json library for handling JSON data

# API key for IntelX API, retrieved from an environment variable or defaults to a specified key if not set
# I used it here I made a free trial for the task So we can use
API_KEY = os.getenv("INTELX_API_KEY", "6173b3dd-4892-49d1-b77a-b2b2ea83a244")

# URL to initiate a search on IntelX
API_URL = "https://2.intelx.io/intelligent/search"

# URL to check the results of a search on IntelX
RESULT_URL = "https://2.intelx.io/intelligent/search/result"


# Function to start a dark web search with a specified search term
def search_darkweb(term):
    headers = {"x-key": API_KEY}  # Headers with API key for authorization
    data = {"term": term, "bucket": "darknet", "timeout": 30}  # Payload for the search request

    # Make a POST request to initiate the search on IntelX API
    response = requests.post(API_URL, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Extract the task ID from the response JSON
            task_id = response.json().get("id")
            print(f"Search START. Task ID: {task_id}")  # Log the task ID
            return check_search_results(task_id)  # Start checking results with the task ID
        except ValueError:
            # Handle cases where response is not in JSON format
            print("Error: Response is not JSON format.")
            return None
    else:
        # Print an error if the search initiation fails
        print(f"Error STARTING the search: {response.status_code} - {response.text}")
        return None


# Function to check the results of a search using the task ID
def check_search_results(task_id, max_wait=180):
    headers = {"x-key": API_KEY}  # Headers with API key for authorization
    elapsed = 0  # Track how long we've been waiting for results

    # Loop until max_wait is reached or results are ready
    while elapsed < max_wait:
        # Make a GET request to check the search results
        response = requests.get(f"{RESULT_URL}?id={task_id}", headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Confirm that response is in JSON format
            if response.headers.get("Content-Type") == "application/json":
                # Parse the JSON response data
                data = response.json()
                print(f"Status check at {elapsed}s: {json.dumps(data, indent=2)}")  # Log formatted response data

                # Check if the search is complete (status 2)
                if data.get("status") == 2:
                    return data  # Return the completed search data
                elif data.get("status") == 3:
                    # Handle cases where an error occurred in the search
                    print(f"Error in search task: {data}")
                    return None
                else:
                    # If search is still in progress, wait and check again
                    print("Search in progress, waiting 5 seconds...")
                    time.sleep(5)  # Wait for 5 seconds before checking again
                    elapsed += 5  # Increment elapsed time by 5 seconds
            else:
                # Print an error if the response is not JSON
                print("Error: Response is not JSON format.")
                return None
        else:
            # Print an error if the result request fails
            print(f"Error fetching results: {response.status_code} - {response.text}")
            return None

    # If max_wait time is exceeded, print a message and stop checking
    print(f"Max wait time exceeded. Task ID: {task_id}. Please try again later.")
    return None


# Usage of the dark web search function
domain_to_search = "ynet.co.il"  # domain to search for
data = search_darkweb(domain_to_search)  # Start the search and get results

# Check if data is available and print search completion message
if data:
    print("Search completed.")
else:
    print("No results found or an error")
