# Flask API for Berry Statistics

This Flask API provides statistics and a histogram for berry growth times using data from the PokeAPI.
## Prerequisites
You can find the in the file requirements.txt
- Python 3.11
- Flask 
- httpx 
- matplotlib 


## Usage

To use the Berries API, you can make HTTP GET requests to the following endpoints:

- `/allBerryStats`: Retrieves statistics about berries.

- `/histogram`: Displays a histogram of berry growth frequencies.

## Request Headers

Make sure to include the following headers in your requests:

- `Content-Type: application/json`: This header specifies that the request and response content is in JSON format.

## Example Usage

### Retrieve statistics about berries

**Endpoint**: `/allBerryStats`

**Method**: GET

**Response Format**: JSON

**Example Request**:

`http
GET /allBerryStats HTTP/1.1
Content-Type: application/json`
Host: <your-api-host>```

**Example Request**:
{
  "berries_names": ["berry1", "berry2", ...],
  "min_growth_time": 2,
  "median_growth_time": 4,
  "max_growth_time": 8,
  "variance_growth_time": 6,
  "mean_growth_time": 4.5,
  "frequency_growth_time": {
    "2": 3,
    "4": 5,
    "6": 2,
    "8": 1
  }
}

### View the berry growth time histogram
Endpoint: /histogram

Method: GET

Response Format: HTML with an embedded image

Example Request: