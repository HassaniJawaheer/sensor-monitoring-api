import json
import requests

data_path = "data/sample_measurements.json"
url = "http://127.0.0.1:8000/measures/"

with open(data_path) as file:
    data = json.load(file)

for payload in data:
    response = requests.post(url, json=payload)
    print(response.status_code)