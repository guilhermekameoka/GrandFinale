import json
import urllib3
import boto3
import http.client
import configparser



def lambda_handler(event, context):
    """
    Builds a response based on label or face detection

    Attributes
    ----------
    event: dict
        serveless event
    detect_type: str
        Value passed to Rekognition (detect_labels, detect_faces)
    label_field: str
        Label name for json key
    """
    try:
        ebody = event.get('body')
        if not ebody:
            raise ValueError('Empty body received!! Please try again.')

        print(json.dumps(ebody))

        client = boto3.client('lexv2-runtime')
        response = client.put_session(
            responseContentType= 'text/plain; charset=utf-8',
            botId = ebody['bot']['id'],
            botAliasId = ebody['bot']['aliasId'],
            localeId = ebody['bot']['localeId'],
            sessionId = ebody['sessionId'],
            sessionState = ebody['sessionState'],
            messages = [
                {
                    "contentType":"PlainText",
                    "content": "testando"
                }]
        )

        # putSession({
        # responseContentType: 'text/plain; charset=utf-8',
        # botId: '',
        # botAliasId: '',
        # localeId: 'en_US',
        # sessionId: '',
        # sessionState: {
        #     dialogAction: { type: 'Delegate' },
        #     intent: { name: 'Intent', state: 'InProgress' },
        #     sessionAttributes: { test: 'test' }
        # }
        # }

    
    except Exception as e:
        return e



    response = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": json.dumps(ebody)}

    return response