# -*- coding: utf-8 -*-
import json
import requests

import sys
import codecs


#page_id = "056e94dd356f46b3b78feb005189ad97"
#page_id = "63234c3f6a254bf7a46d6510b144b8c6"
page_id = "82b78f8b232a40cc8154f36483d45907"
page_id ="481c79b3-f4a1-4eb5-9c19-6945ef71142a"
page_id ='ddca7c73-10c9-44de-8b82-3dbea27bffe9'

page_id = '20dd09ced3ca4aef93a58673d1d7a0cb'
#page_id = '60ba1212-6423-4c9a-9d42-929eaf86322f'
#url = f"https://api.notion.com/v1/pages/{page_id}" #for pageid
url = f"https://api.notion.com/v1/blocks/{page_id}/children" #for blockid

token = "secret_9ml5fh1fi8KEKffPhwRLfOMEbJldRrQp61LRVwZTDFo"

headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2021-08-16"
}

response = requests.request("GET", url, headers=headers)
json_loaded = json.dumps(response.text)
#print(response.status_code)
#print(type(response.text))
#print(json_loaded)

with open("../output_text_3.json", "w", encoding="utf-8") as f:
    f.write(response.text)