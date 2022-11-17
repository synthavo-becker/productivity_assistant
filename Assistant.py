text_in_Block = input()

import requests
import json
import pandas as pd
import urllib.request
from urllib.error import URLError
import time
from progress.bar import IncrementalBar
from tools import secret
import clipboard
import copy


"""
Ýou need to have a file called "secret.py" in the tools folder:

jo
"""


url = "https://api.notion.com/v1/pages"

headers = {
    "Authorization": "Bearer " + secret.token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}


status_general = {
    'id':'%5EOE%40',
    'type':'select',
    'select': {
        'id':'1',
        'name':'General',
        'color':'red'
    }
}
status_HR = {
    'id':'%5EOE%40',
    'type':'select',
    'select': {
        'id':'3',
        'name':'HR',
        'color':'green'
    }
}
status_Sales = {
    'id':'%5EOE%40',
    'type':'select',
    'select': {
        'id':'2',
        'name':'Sales',
        'color':'yellow'
    }
}
status_Dev = {
    'id':'%5EOE%40',
    'type':'select',
    'select': {
        'id':'2ee71963-e2e1-45b4-b093-d6b59109e4d5',
        'name':'Dev',
        'color':'purple'
    }
}






def get_clipboard():
    return clipboard.paste()


if __name__ =="__main__":

    

    
    text_in_Block = text_in_Block.lower()
    
    if text_in_Block.startswith("anki"): #anki mode
        pass
    else: #notion mode, default 

        
        if text_in_Block.startswith("hr"):
            status = status_HR
            text_in_Block = text_in_Block[2:]
        elif text_in_Block.startswith("dev"):
            status = status_Dev
            text_in_Block = text_in_Block[3:]
        elif text_in_Block.startswith("sales"):
            status = status_Sales
            text_in_Block = text_in_Block[5:]
        else:
            status = status_general
            

            
    
        data = {
            "parent": { "database_id": secret.db_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text":{
                                "content": text_in_Block
                            }
                        }
                    ]
                },
                "Status": status
            }

        }


        data = json.dumps(data)

        response = requests.request("POST", url, headers=headers, data=data)

        #if(response.status_code != 200):
            #print(f"response: {response.status_code}")
            #print(response.text)
            #waiting = input()

        print(response)


