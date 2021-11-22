import json
import requests

#page_id = "056e94dd356f46b3b78feb005189ad97"
page_id = "63234c3f6a254bf7a46d6510b144b8c6"
url = f"https://api.notion.com/v1/pages/{page_id}"

token = "secret_9ml5fh1fi8KEKffPhwRLfOMEbJldRrQp61LRVwZTDFo"

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2021-05-13"
}

response = requests.request("GET", url, headers=headers)
json_loaded = json.dumps(response.text)
print(response.status_code)
print(type(response.text))
print(json_loaded)

with open("../output_text.json", "w") as f:
    f.write(response.text)