from flask import Flask
import json
import statistics
import httpx
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

API_URL = "https://pokeapi.co/api/v2/berry/?offset=0&limit=80"
GROWTH_TIMES_CACHE = {}

http_client = httpx.Client()


def get_berries_names():
    """Retrieve names of all berries from API, and returns a list"""

    response = http_client.get(API_URL)
    response.raise_for_status()

    data = response.json()
    results = data["results"]
    return [result["name"] for result in results]


def get_growth_time(name):
    """Retrieve growth time for specific name berrie from API"""

    if name in GROWTH_TIMES_CACHE:
        return GROWTH_TIMES_CACHE[name]
    url = f"https://pokeapi.co/api/v2/berry/{name}/"
    response = http_client.get(url)
    response.raise_for_status()

    data = response.json()
    growth_time = data["growth_time"]
    GROWTH_TIMES_CACHE[name] = growth_time
    return growth_time



def get_all_growth_times(berries_names):
    """Executes at the same time, retrieval of all berries growth time"""

    with ThreadPoolExecutor() as excecutor:
        growth_times = list(excecutor.map(get_growth_time, berries_names))

    return growth_times


def get_frequency_growth_time(growth_times):
    """Calculates frequency of growth times and returns a dictionary"""

    freq = {}
    for time in growth_times:
        if time in freq:
            freq[time] += 1
        else:
            freq[time] = 1
    return freq


berry_names = get_berries_names()
all_growth_times = get_all_growth_times(berry_names)
min_growth_time = min(all_growth_times)
median_growth_time = statistics.median(all_growth_times)
max_growth_time = max(all_growth_times)
variance_growth_time = statistics.variance(all_growth_times)
mean_growth_time = statistics.mean(all_growth_times)
frequency_growth_time = get_frequency_growth_time(all_growth_times)


@app.route("/", methods=['GET'])
def get_berries():
    """Returns json response to endpoint request of berries statistics"""
    result = {"berries_names": berry_names,
              "min_growth_time": min_growth_time,
              "median_growth_time": median_growth_time,
              "max_growth_time": max_growth_time,
              "variance_growth_time": variance_growth_time,
              "mean_growth_time": mean_growth_time,
              "frequency_growth_time": frequency_growth_time
              }
    json_data = json.dumps(result)
    return json_data


if __name__ == "__main__":
    app.run(debug=True)