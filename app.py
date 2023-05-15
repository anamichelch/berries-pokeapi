from flask import Flask, make_response
import json
import statistics
import httpx
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

API_URL = "https://pokeapi.co/api/v2/berry/?offset=0&limit=80"
BERRIE_NAMES_CACHE = {}
GROWTH_TIMES_CACHE = {}
CACHE_TIME_EXPIRATION = timedelta(minutes=2)


def get_berries_names():
    """Retrieve names of all berries from API, and returns a list"""
    timestamp = datetime.utcnow()
    http_client = httpx.Client(timeout=httpx.Timeout(30.0))

    if BERRIE_NAMES_CACHE and BERRIE_NAMES_CACHE["timestamp"] - datetime.utcnow() <= CACHE_TIME_EXPIRATION:
        return BERRIE_NAMES_CACHE["data"]

    response = http_client.get(API_URL)
    response.raise_for_status()

    data = response.json()
    results = data["results"]
    berries_names = [result["name"] for result in results]
    BERRIE_NAMES_CACHE["data"] = berries_names
    BERRIE_NAMES_CACHE["timestamp"] = timestamp

    return berries_names


def get_growth_time(name):
    """Retrieve growth time for specific name berrie from API"""
    timestamp = datetime.utcnow()
    http_client = httpx.Client(timeout=httpx.Timeout(30.0))

    if name in GROWTH_TIMES_CACHE:
        grow_time, timestamp = GROWTH_TIMES_CACHE[name]
        if datetime.utcnow() - timestamp <= CACHE_TIME_EXPIRATION:
            return grow_time
    url = f"https://pokeapi.co/api/v2/berry/{name}/"
    response = http_client.get(url)
    response.raise_for_status()

    data = response.json()
    growth_time = data["growth_time"]
    GROWTH_TIMES_CACHE[name] = (growth_time, timestamp)

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


@app.route("/", methods=['GET'])
def get_berries_stats():
    """Returns json response to endpoint request of berries statistics"""
    berry_names = get_berries_names()
    all_growth_times = get_all_growth_times(berry_names)
    min_growth_time = min(all_growth_times)
    median_growth_time = statistics.median(all_growth_times)
    max_growth_time = max(all_growth_times)
    variance_growth_time = statistics.variance(all_growth_times)
    mean_growth_time = statistics.mean(all_growth_times)
    frequency_growth_time = get_frequency_growth_time(all_growth_times)

    result = {"berries_names": berry_names,
              "min_growth_time": min_growth_time,
              "median_growth_time": median_growth_time,
              "max_growth_time": max_growth_time,
              "variance_growth_time": variance_growth_time,
              "mean_growth_time": mean_growth_time,
              "frequency_growth_time": frequency_growth_time
              }
    json_data = json.dumps(result)

    # Set the content-type header to "application/json"
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'

    return response


def create_histogram():
    """ Returns a Histogram image in html , of the berries growth frequencies"""

    berry_names = get_berries_names()
    all_growth_times = get_all_growth_times(berry_names)
    data = all_growth_times

    # Create a histogram of the growth times
    plt.hist(data, bins=range(min(data), max(data) + 2, 1), align='left', edgecolor='black')
    plt.xticks(range(min(data), max(data) + 1))
    plt.xlabel('Growth Time (hours)')
    plt.ylabel('Frequency')
    plt.title('Growth Time Histogram')

    plt.savefig('static/growth_time_histogram.png')


@app.route("/histo", methods=['GET'])
def show_histogram():
    create_histogram()
    return '<img src="/static/growth_time_histogram.png">'


if __name__ == "__main__":
    app.run(debug=True)
