from flask import Flask
import requests
import json

app = Flask(__name__)
API_URL = "https://pokeapi.co/api/v2/berry/"
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()

else:
    print(f"The request failed with status code: {response.status_code}")

#Response: {
#    "berries_names": [...],
#    "min_growth_time": "" // time, int
#    "median_growth_time": "", // time, float
#    "max_growth_time": "" // time, int
#    "variance_growth_time": "" // time, float
#    "mean_growth_time": "", // time, float
#    "frequency_growth_time": "", // time, {growth_time: frequency, ...}
#}


def get_berries_names(data):
    results = data["results"]
    berries_names = []
    for result in results:
        berries_names.append(result["name"])

    return berries_names

def get_growth_times(data):
    for i in range(len(berry_names)):
        url = "https://pokeapi.co/api/v2/berry/{i}/"

    return pass

berry_names = get_berries_names(data)

@app.route("/",methods = ['GET'])
def get_berries():
    result = {"berries_names": berry_names}
    json_data = json.dumps(result)
    return json_data


