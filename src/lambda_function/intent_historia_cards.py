import json
import urllib3
from functions import *
import random
from unicodedata import normalize


    
#Checks for slots, validates values and return cards in case values are not valid
def validate_type_card(event, slots):

    valids = ['gato', 'cachorro', 'abelha', 'galinha', 'chuvoso','ensolarado','nublado','trovejando','aviao','bicicleta','carro','navio','foguete','espaco','floresta','mar','praia']


    protagonists = {
        'gato':'https://sprint8pd.s3.amazonaws.com/gato.jpg',
        'cachorro':'https://sprint8pd.s3.amazonaws.com/cachorro.jpg',
        'abelha': 'https://sprint8pd.s3.amazonaws.com/abelha.jpg',
        'galinha': 'https://sprint8pd.s3.amazonaws.com/galinha.jpg'
    }

    clima = {
        'chuvoso':'https://sprint8pd.s3.amazonaws.com/clima/chuvoso.jpg',
        'ensolarado':'https://sprint8pd.s3.amazonaws.com/clima/ensolarado.jpg',
        'nublado':'https://sprint8pd.s3.amazonaws.com/clima/nublado.jpg',
        'trovejando':'https://sprint8pd.s3.amazonaws.com/clima/trovejando.jpg'
    }

    veiculo = {
        'avião':'https://sprint8pd.s3.amazonaws.com/veiculo/aviao.jpg',
        'bicicleta':'https://sprint8pd.s3.amazonaws.com/veiculo/bicicleta.jpg',
        'carro':'https://sprint8pd.s3.amazonaws.com/veiculo/carro.jpg',
        'navio':'https://sprint8pd.s3.amazonaws.com/veiculo/navio.jpg',
        'foguete':'https://sprint8pd.s3.amazonaws.com/veiculo/foguete.jpg'
    }

    local = {
        'espaço':'https://sprint8pd.s3.amazonaws.com/local/espaco.jpg',
        'floresta':'https://sprint8pd.s3.amazonaws.com/local/floresta.jpg',
        'mar':'https://sprint8pd.s3.amazonaws.com/local/mar.jpg',
        'praia':'https://sprint8pd.s3.amazonaws.com/local/praia.jpg'

    }


    #returns invalidSlot if it's missing
    isMissing = check_missing_slot(slots, "card1", "PlainText", "Quem será o protagonista da história?") 

    if isMissing: 

        for key in protagonists:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": key,
                    "value": normalize('NFKD', key).encode('ASCII','ignore').decode('ASCII')
                }
            ]
            imageUrl = protagonists[key]
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

        return isMissing
    
    # Validating the inputs
    # if slots['card1']['value']['originalValue'] not in valids:
    #     response = build_response('card1', 'Selecione um cartão')
    #     return response
    
    isMissing = check_missing_slot(slots, "card2", "PlainText", "Como está o dia?") 

    if isMissing: 

        for key in clima:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": key,
                    "value": normalize('NFKD', key).encode('ASCII','ignore').decode('ASCII')
                }
            ]
            imageUrl = clima[key]
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

        return isMissing
    
    isMissing = check_missing_slot(slots, "card3", "PlainText", "Vamos usar um veículo?") 

    if isMissing: 

        for key in veiculo:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": key,
                    "value": normalize('NFKD', key).encode('ASCII','ignore').decode('ASCII')
                }
            ]
            imageUrl = veiculo[key]
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))

        return isMissing
    
    isMissing = check_missing_slot(slots, "card4", "PlainText", "Você pensou em um local?") 

    if isMissing: 

        for key in local:

            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": key,
                    "value": normalize('NFKD', key).encode('ASCII','ignore').decode('ASCII')
                }
            ]
            imageUrl = local[key]
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
