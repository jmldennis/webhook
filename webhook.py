import requests
from flask import Flask, request, json
import pdb
import random


app = Flask(__name__)
port = 5000

def create_webhook(url,token):
    webhooks_api = 'https://webexapis.com/v1/webhooks'
    headers = {
        "Content-Type":"application/json",
        "Accept":"application/json",
        "Authorization":"Bearer " + token
    }
    data = { 
        "name": "Webhook to ChatBot",
        "resource": "all",
        "event": "all",
        "targetUrl": url
    }
    response = requests.post(webhooks_api, headers=headers, data=json.dumps(data))
        
    return response


def delete_webhook(token):
    webhooks_api = 'https://webexapis.com/v1/webhooks'
    headers = {
        "Content-Type":"application/json",
        "Accept":"application/json",
        "Authorization":f"Bearer {token}"
    }

    response = requests.get(webhooks_api,headers=headers).json()

    for webhook in response["items"]:
        print(f"Deleting {webhook.get('id')}")
        webhooks_api = f'https://webexapis.com/v1/webhooks/{webhook.get("id")}'
        requests.delete(webhooks_api,headers=headers)

    return response



@app.route('/', methods=['GET', 'POST'])
def index():
    global token
    """Receive a notification from Webex Teams and handle it"""
    if request.method == 'GET':
        return (f'Request received on local port {port}',200)
    elif request.method == 'POST':
        if 'application/json' in request.headers.get('Content-Type'):
            # Notification payload, received from Webex Teams webhook
            data = request.get_json()

            # Loop prevention, ignore messages which were posted by bot itself.
            # The bot_id attribute is collected from the Webex Teams API
            # at object instatiation.
            url = "https://webexapis.com/v1/people/me"
            headers = {
                    "Content-Type":"application/json",
                    "Accept":"application/json",
                    "Authorization":"Bearer " + token
                }
            response = requests.get(url,headers=headers).json()
            bot_id = response["id"]

            if bot_id == data.get('data').get('personId'):
                return 'Message from self ignored'

            else:
                # Collect the roomId from the notification,
                # so you know where to post the response
                # Set the msg object attribute.
                room_id = data.get('data').get('roomId')
                
                # Collect the message id from the notification, 
                # so you can fetch the message content
                message_id = data.get('data').get('id')

                url = "https://webexapis.com/v1/messages"
                headers = {
                    "Content-Type":"application/json",
                    "Accept":"application/json",
                    "Authorization":"Bearer " + token
                }
                my_responses = ["Steve","Steeeeve","Steeeeeeeeeeeeeveeee!"]
                data = { 
                    "roomId":room_id,
                    "text":random.choice(my_responses)
                }
                response = requests.post(url, headers=headers, data=json.dumps(data))


                return (data,200)
        else: 
            return ('Wrong data format', 400)


if __name__ == '__main__':
    #Url for the webhook to hit (NGROK URL)
    url = 'url'
    #Webex Access Token
    token = 'token'

    response = delete_webhook(token)
    response = create_webhook(url,token)
    app.run(host="0.0.0.0", port=port, debug=True)