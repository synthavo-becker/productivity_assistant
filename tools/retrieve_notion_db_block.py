import requests
import json 

database_id = "326c3d22565c4473982d6f935e28cfff"

url = f"https://api.notion.com/v1/databases/{database_id}/query"

payload = {"page_size": 200}
token = ""
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

json_loaded = json.loads(response.text)

x = json_loaded['results'][0]['properties']['Task']['title'][0]['text']
y = [json_loaded['results'][t]['properties']['Task']['title'][0]['text']["content"] for t in range(len(json_loaded["results"])-1)]
#print(x)

searched_string = "Urlaubs"
for index, item in enumerate(y):
    if searched_string in item:
        print("HIIIIER")
        print(index)
print("ji")