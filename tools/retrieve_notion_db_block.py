import requests
import json 
import secret

database_id = secret.db_id

url = f"https://api.notion.com/v1/databases/{database_id}/query"

payload = {"page_size": 200}
token = secret.token
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

json_loaded = json.loads(response.text)


x = json_loaded['results'][0]['properties']
y = [json_loaded['results'][t]['properties']['Task']['title'][0]['text']["content"] for t in range(len(json_loaded["results"])-1)]
#print(x)

searched_string = "Urlaubs"
for index, item in enumerate(y):
    if searched_string in item:
        print("HIIIIER")
        print(index)
print("ji")