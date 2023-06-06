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
from tools import status_db as db

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









def get_clipboard():
    return clipboard.paste()


def standard_processing(text_in_Block):
    
    start_strings = text_in_Block.split(" ")[:2]

    status_mapping = {
        "hr": db.status_HR,
        "dev": db.status_Dev,
        "sales": db.status_Sales
    }
    prio_mapping = {
        "aa": db.PRIO_TODAY,
        "a" : db.PRIO_HIGH,
        "b": db.PRIO_MID,
        "c": db.PRIO_LOW
    }
    selected_status = None
    selected_prio = None

    for status in status_mapping:
        if status in start_strings:
            selected_status = status_mapping[status]

            #remove status from the string
            if status == start_strings[0]:
                text_in_Block = text_in_Block[len(status) + 1:]
            elif status == start_strings[1]:
                text_in_Block = text_in_Block[:len(start_strings[0]) + 1] +  text_in_Block[len(start_strings[0]) + 1 + len(status) + 1:]
            break

    

    start_strings = text_in_Block.split(" ")[:1]

    for prio in prio_mapping:
        if prio in start_strings:
            selected_prio = prio_mapping[prio]

            #remove prio from the string
            text_in_Block = text_in_Block[len(prio) + 1:]
            break
    
    #if not found, select standards
    if selected_status is None:
        selected_status = db.status_general
    if selected_prio is None:
        selected_prio = db.PRIO_LOW        

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
            "Status": selected_status,
            "Prio": selected_prio
        }
    }


    data = json.dumps(data)

    response = requests.request("POST", url, headers=headers, data=data)

    if(response.status_code != 200):
        print(f"response: {response.status_code}")
        print(response.text)
        waiting = input()
    else:
        print("200")



if __name__ =="__main__":

    text_in_Block = text_in_Block.lower()
    
    if text_in_Block.startswith("anki"): #anki mode
        pass
    if text_in_Block.startswith("miro"): #miro mode
        clipboard_text = get_clipboard()
        splitted = clipboard_text.split("\n")
        for line in splitted:
            line = line.lower()
            standard_processing(line)
    else: #notion mode, default
        standard_processing(text_in_Block)
       


