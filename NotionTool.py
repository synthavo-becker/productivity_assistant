import requests
import json
import win32clipboard
import urllib.request

#blockid = "ce6dfa0443ea47a49c95066b0dbe3989"
db_id = "326c3d22565c4473982d6f935e28cfff"

url = "https://api.notion.com/v1/pages"
token = "secret_9ml5fh1fi8KEKffPhwRLfOMEbJldRrQp61LRVwZTDFo"

headers = {
    "Authorization": "Bearer " + token,
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
    def __str__(self):
        return(self.head + "\n" + self.content)



def parse_cards(data):
    cards = []
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
                current_card.content = current_card.content + row

    cards.append(current_card)
    return cards




def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
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

def choose_deck(decks):
    
    print("Choose deck:")
    for index, deck in enumerate(decks): print(f"{index}: {deck}")
    chosen_one = input()
    try:
        ret = int(chosen_one)
        if ret >= len(decks) or ret < 0 :
            return choose_deck
        else: 
            return ret 
    except: 
        return choose_deck

def create_card(deckname, front, back):
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
                }
            }
        }
    }
    result = invoke(API_base["action"],  **API_base["params"])


def anki():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    data = data.split("\n") # split by line

    cards = parse_cards(data)

    decks = invoke('deckNames') 
    chosen_deck = choose_deck(decks)

    
    for card in cards:
        create_card(decks[chosen_deck], card.head, card.content)

    


if __name__ =="__main__":

    text_in_Block = input()
    text_in_Block = text_in_Block.lower()
    
    if text_in_Block.startswith("anki"): #anki mode
        anki()
    else: #notion mode, default 
        if text_in_Block.startswith("td") or text_in_Block.startswith("today"):
            text_in_Block = text_in_Block[2:len(text_in_Block)]
            chosen_status = status_today
        else:
            chosen_status = status_todo
        data = {
            "parent": { "database_id": db_id},
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
                "Status": chosen_status
            }

        }


        data = json.dumps(data)

        response = requests.request("POST", url, headers=headers, data=data)

        if(response.status_code != 200):
            print(f"response: {response.status_code}")
            print(response.text)
            waiting = input()


