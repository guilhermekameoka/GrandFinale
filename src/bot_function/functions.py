import json
import urllib3
import http.client
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('bot.conf')

KEY_API=config['BOT']['KEY_API']
BUCKET_IMAGES = config['BOT']['BUCKET_IMAGES']

def json_bucket_images (json_info):
    for key in json_info:
        for value in json_info[key].values():
            value['link'] = value['link'].replace('meu_bucket', BUCKET_IMAGES)
    
    return json_info

#checks if there are missing slots and returns the slot to elicit
def check_missing_slot(slots, invalidSlot, contentType, content, force_return = False):

    if not slots[invalidSlot] or force_return == True:
        return {
            'valid': False,
            'invalidSlot': invalidSlot,
            'messages': [
                {
                    "contentType":contentType,
                    "content": content,
                }
            ]
        }
    else:
        return False 

#if the values are not valide, builds a responsecard to the slot to elicit 
def build_responsecard (invalidSlot, contentType, content, subtitle, buttons, imageUrl = None ):

    response = {
        "valid": False,
        "invalidSlot": invalidSlot,
        "messages": [
            {
                "contentType": contentType,
                "content": content,
                contentType[0].lower() + contentType[1:]: {
                    "title": " ",
                    "subtitle": " ",
                    "imageUrl": imageUrl,
                    "buttons": buttons
                }
            }
        ]
    }

    return response


def build_message (contentType, subtitle, buttons, imageUrl = None ):
    message = {
        "contentType": contentType,
        contentType[0].lower() + contentType[1:]: {
            "title": " ",
            "subtitle": subtitle,
            "imageUrl": imageUrl,
            "buttons": buttons
        }
    }
    return message

def build_response(invalidSlot, content):

    response = {
        "valid": False,
        "invalidSlot": invalidSlot,
        "messages": [
            {
                "contentType": "PlainText",
                "content": content
            }
        ]
    }

    return response

#build a response based on validation value, valid or invalid
def check_validation (validation, intent, slots):

    if validation['valid'] == False:

        response = {
            "sessionState": {
                "dialogAction": {
                    "slotToElicit": validation['invalidSlot'],
                    "type": "ElicitSlot"
                },
                "intent": {
                    "name": intent,
                    "slots": slots
                }
            },
            "messages": validation['messages']
        }
    else:

        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    "name": intent,
                    "slots": slots
                }
            }
        }
    
    return response

#sessionState type close and state flfilled
def close_session(intent, slots):
    sessionState = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent,
                "slots": slots,
                "state": "Fulfilled"
            }
        }
    }
    return sessionState


def end_card(title):

    rescard_title = title
    rescard_buttons = [
        {
            "text": 'Desenho - Foto',
            "value": 'desenho'
        },
        {
            "text": 'Cartões',
            "value": 'cartões'
        },
        {
            "text": 'Expressar',
            "value": 'expressar'
        },
    ]
    imageUrl = 'https://sprint8pd.s3.amazonaws.com/bot.jpg'
    return (build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

    
def create_story_function (phrase, id_model):

    http = urllib3.PoolManager()
    url = 'https://api.openai.com/v1/chat/completions'

    Headers = {'Authorization' : f'Bearer {KEY_API}', 'Content-Type': 'application/json'}
    payload = {'model': id_model, 'messages': [{'role': 'user', 'content': phrase}]}

    encoded_body = json.dumps(payload)
    res = http.request('POST', url, body=encoded_body, headers=Headers)
    respo = ''
    if res.status == 200:
        respo = json.loads(res.data)

    story = respo['choices'][0]['message']['content']

    return story

def create_audio (phrase, voice):

    http = urllib3.PoolManager()
    url = "https://4fa70odtzi.execute-api.us-east-1.amazonaws.com/polly"

    Headers = {'Content-Type': 'application/json'}
    payload = {
        "phrase": phrase,
        "voice": voice
    }

    encoded_body = json.dumps(payload)
    res = http.request('POST', url, body=encoded_body, headers=Headers)
    response = ''

    if res.status == 200:
        response = json.loads(res.data)

    return response



#translates for the language selected
def translate(text, language = 'pt-br'):

    try:

        conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")

        payload = [
            {
                "Text": text
            }
        ]

        headers = {
            'content-type': "application/json",
            'X-RapidAPI-Key': "b2fb28a07dmsh10b46f524a93a0fp160844jsn41bda9f18e97",
            'X-RapidAPI-Host': "microsoft-translator-text.p.rapidapi.com"
        }

        if(language == 'pt-br'):
            conn.request("POST", "/translate?to%5B0%5D=pt-br&api-version=3.0&profanityAction=NoAction&textType=plain", json.dumps(payload), headers)
        
        else:
            conn.request("POST", "/translate?to%5B0%5D=en&api-version=3.0&from=pt-br&profanityAction=NoAction&textType=plain", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()

        response = json.loads(data.decode('utf-8'))
        translated_text = response[0]['translations'][0]['text']

        return translated_text
    
    except:

        return text