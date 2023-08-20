import json
import urllib3
from functions import *
import random

    
#Checks for slots, validates values and return cards in case values are not valid
def validate_type_card(event, slots):

    valid_types = ['kommunicateMediaEvent']

    #returns invalidSlot if it's missing
    isMissing = check_missing_slot(slots, "historia", "PlainText", "Insira uma imagem, um link ou tire uma foto do seu desenho") 
    if isMissing: return isMissing

    if slots['historia']['value']['originalValue'] not in valid_types:

        if "http" not in slots['historia']['value']['originalValue']:

            content = "Por favor selecione uma imagem"
            response = build_response("historia", content)

            return response
        
    elif 'image' not in str(json.loads(event['requestAttributes']['attachments'])[0]['type']):
        print(str(json.loads(event['requestAttributes']['attachments'])[0]['type']))

        content = "Por favor selecione um tipo de arquivo de imagem"
        response = build_response("historia", content)

        return response
   
    return {'valid': True}


def ObterHistoria_handler(event):

    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    
    response = {}

    validation = validate_type_card(event, slots)

    #checks validation and invalid slots
    if event['invocationSource'] == 'DialogCodeHook':

        response = check_validation(validation, intent, slots)
        return response

    #all slots are valid
    if event['invocationSource'] == 'FulfillmentCodeHook':

        slot_historia = slots['historia']['value']['originalValue']
        
        try:
            imageURL = str(json.loads(event['requestAttributes']['attachments'])[0]['payload']['url'])

        except:
            imageURL = slot_historia

        http = urllib3.PoolManager()
        url = "https://4fa70odtzi.execute-api.us-east-1.amazonaws.com/rekognition/v1"

        Headers = {'Content-Type': 'application/json'}
        payload = {
            "bucket": "sprint8pd",
            "imageURL": imageURL,
            "imageName": "imageTest2.jpg"
        }

        encoded_body = json.dumps(payload)
        res = http.request('POST', url, body=encoded_body, headers=Headers)
        respo = ''


        if res.status == 200:
            respo = json.loads(res.data)

        labels = []
        for label in respo['labels']:
            labels.append(label['Name'])

        if len(labels) == 0:
            labels = ['Hero']

        translated_labels = ",".join(labels)
        translated_labels = translate(translated_labels)
        translated = translated_labels.split(',')

        print(translated)    
        
        #random index----------------------------------------
        rand_number = lambda: random.randint(0, len(labels)-1)
        #----------------------------------------------------

        label1 = translated[rand_number()]
        label2 = translated[rand_number()]
        label3 = translated[rand_number()]
        label4 = translated[rand_number()]

        id_model = 'gpt-3.5-turbo'
        phrase = f'crie uma história infantil bem curta, máximo de 500 caracteres e não ultrapasse 80 palavras, que contenha os seguintes elementos: {label1},{label2},{label3},{label4}'

        story = create_story_function(phrase, id_model)

        voice = ['Camila','Thiago']
        audio_creation = create_audio(story,voice[random.randint(0, len(voice)-1)])

        audio = audio_creation['url_to_audio']

        audio_kommunicate = {
            "message": "<audio controls src='"+audio+"'></audio>",
            "platform": "kommunicate",
            "messageType": "html"
        }

        response = {
            "messages": [
                {
                    "contentType":"PlainText",
                    "content": story
                },
                {
                    "contentType":"CustomPayload",
                    "content": json.dumps(audio_kommunicate)
                },
                {
                    "contentType":"PlainText",
                    "content": "Posso ajudar em algo mais?"
                }

            ]
        }
        sessionState = close_session(intent, slots) 
        response.update(sessionState)
    
    return response
