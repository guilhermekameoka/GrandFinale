import json
from functions import *
import random

    
#Checks for slots, validates values and return cards in case values are not valid
def validate_type_card(event, slots):

    valores = json_bucket_images(json.load(open('json_files/intent_historia_cards_info.json')))

    #returns invalidSlot if it's missing
    isMissing = check_missing_slot(slots, "card1", "PlainText", "Escolha o protagonista da história, ou escreva um nome!") 

    if isMissing: 

        for key in valores['protagonists']:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": valores['protagonists'][key]['texto'],
                    "value": key
                }
            ]
            imageUrl = valores['protagonists'][key]['link']
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

        return isMissing
    
    
    isMissing = check_missing_slot(slots, "card2", "PlainText", "Como está o dia?") 

    if isMissing: 

        for key in valores['clima']:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": valores['clima'][key]['texto'],
                    "value": key
                }
            ]
            imageUrl = valores['clima'][key]['link']
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

        return isMissing
    
    isMissing = check_missing_slot(slots, "card3", "PlainText", "Vamos usar um veículo?") 

    if isMissing: 

        for key in valores['veiculo']:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": valores['veiculo'][key]['texto'],
                    "value": key
                }
            ]
            imageUrl = valores['veiculo'][key]['link']
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

        return isMissing
    
    isMissing = check_missing_slot(slots, "card4", "PlainText", "Você pensou em um local?") 

    if isMissing: 

        for key in valores['local']:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": valores['local'][key]['texto'],
                    "value": key
                }
            ]
            imageUrl = valores['local'][key]['link']
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

        return isMissing


    return {'valid': True}


def ObterHistoriaCards_handler(event):

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

        card1 = slots['card1']['value']['originalValue']
        card2 = slots['card2']['value']['originalValue']
        card3 = slots['card3']['value']['originalValue']
        card4 = slots['card4']['value']['originalValue']

        id_model = 'gpt-3.5-turbo'
        phrase = f'crie uma história infantil bem curta, máximo de 500 caracteres e não ultrapasse 80 palavras, que contenha os seguintes elementos: {card1},{card2},{card3},{card4}'

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
                }
            ]
        }
        sessionState = close_session(intent, slots) 
        response.update(sessionState)

        final_message = end_card(" ")
        final_message["imageResponseCard"]['title'] = "O que você quer fazer?"
        response['messages'].append(final_message)
    
    return response
