import requests
import json
import urllib.request

API_base = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "API_TEST",
                "modelName": "Basic-7b116",
                "fields": {
                    "Front": "asckwba ",
                    "Back": "ICCCEE <div> was geht</div> "
                }
            }
        }
    }

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


result = invoke(API_base["action"],  **API_base["params"])
anki_base = {
        "action": "cardsInfo",
        "version": 6,
        "params": {
            "cards": [1638031819324,1638031760542]
        }
    }

result_2 = invoke(anki_base["action"],  **anki_base["params"])

print("hii")