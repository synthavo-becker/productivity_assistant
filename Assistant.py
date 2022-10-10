import requests
import json
import pandas as pd
import urllib.request
from urllib.error import URLError
import time
from progress.bar import IncrementalBar
from tools.picture_fetcher import picture_fetcher
from tools.secret import secret
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


status_todo = {
                "id":"^OE@",
                "type":"select",
                "select":{
                    "id":"1"
                    ,"name":"To Do",
                    "color":"red"}
            }

status_today = {
      "id": "^OE@",
      "type": "select",
      "select": {
        "id": "9b329245-fc7d-4257-97d4-0cda03c24dda",
        "name": "TODAY",
        "color": "blue"
      }
    }



class Card:
    def __init__(self, head):
        self.head = head
        self.content = ""
        self.picture_links = []
    def __str__(self):
        return(self.head + "\n" + self.content + "\n" + self.picture_links)



def parse_cards(data, pic_fetcher):
    cards = []
    start_of_picture_row = "![Untitled]"
    
    for counter, row in enumerate(data) :
        if row != '    \r' and row != '\r': # filter empty lines
            #print(repr(row))
            #print("------------------------------------")


            if row.startswith("-"): #these are the headings of the cards
                row = row[1:]
                if counter != 0:
                    cards.append(current_card)
                current_card = Card(row)
            
            else:
                if start_of_picture_row in row:
                    pic_url = pic_fetcher.get_picture_url_of_block(row,current_card.head)
                    current_card.picture_links.append(pic_url)
                else:
                    current_card.content = current_card.content + "<div>" + row + "</div>"
    cards.append(current_card)
    return cards





    
    



def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    try:
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))

        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']
    except URLError:
        print("ANKI NOT ONLINE !")

def choose_deck(decks):
    
    print("Choose ANKI deck:")
    for index, deck in enumerate(decks): print(f"{index}: {deck}")
    chosen_one = input()
    try:
        ret = int(chosen_one)
        if ret >= len(decks) or ret < 0 :
            return choose_deck(decks)
        else: 
            return ret 
    except: 
        return choose_deck(decks)

def send_card_to_anki(deckname, front, back, pic_urls):
    pictures = []
    picture_base = {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/A_black_cat_named_Tilly.jpg/220px-A_black_cat_named_Tilly.jpg",
                "filename": "some_thing.jpg",
                "fields": [
                    "Back"
                ]
            }
    
        
    for pic_url in pic_urls:
        base = copy.deepcopy(picture_base)
        base["url"] = pic_url
        base["filename"] = str(hash(pic_url)) + ".jpg"
        pictures.append(base)

    
        
    
    API_base = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deckname,
                "modelName": "Basic-7b116",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": deckname,
                        "checkChildren": False,
                        "checkAllModels": False
                    }
                },
                "picture" : pictures
            }
        }
    }
    result = invoke(API_base["action"],  **API_base["params"])

def create_all_cards(cards,decks,chosen_deck):
    bar = IncrementalBar('Creating Cards...', max=len(cards))
    for card in cards:
        send_card_to_anki(decks[chosen_deck], card.head, card.content,card.picture_links)
        bar.next()
    bar.finish()

def get_clipboard():
    return clipboard.paste()

def anki():
    data = get_clipboard()
    data = data.split("\n") # split by line

    pic_fetcher = picture_fetcher()
    cards = parse_cards(data,pic_fetcher)

    decks = invoke('deckNames') 
    chosen_deck = choose_deck(decks)

    create_all_cards(cards,decks,chosen_deck)

    

    while(True):
        input("Press Enter to paste Clipboard again.")
        data = get_clipboard()
        data = data.split("\n")  # split by line
        cards = parse_cards(data,pic_fetcher)
        create_all_cards(cards, decks, chosen_deck)


if __name__ =="__main__":

    

    text_in_Block = input()
    text_in_Block = text_in_Block.lower()
    
    if text_in_Block.startswith("anki"): #anki mode
        anki()
    else: #notion mode, default 
        status = {
            'id': '%5EOE%40', 
            'type': 'select', 
            'select': {
                'id': '1',
                'name': 'To Do', 
                'color': 'green'
            }
        }
        data = {
            "parent": { "database_id": secret.db_id},
            "properties": {
                "Task": {
                    "title": [
                        {
                            "text":{
                                "content": text_in_Block
                            }
                        }
                    ]
                },
                "Kategorie": status
            }

        }


        data = json.dumps(data)

        response = requests.request("POST", url, headers=headers, data=data)

        #if(response.status_code != 200):
            #print(f"response: {response.status_code}")
            #print(response.text)
            #waiting = input()

        print(response)


