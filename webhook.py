import requests
from flask import Flask, request, json
import pdb


app = Flask(__name__)
port = 5000

@app.route('/', methods=['GET', 'POST'])
def index():
    """Receive a notification from Webex Teams and handle it"""
    if request.method == 'GET':
        return f'Request received on local port {port}'
    elif request.method == 'POST':
        if 'application/json' in request.headers.get('Content-Type'):
            # Notification payload, received from Webex Teams webhook
            data = request.get_json()
            pdb.set_trace()

            # Loop prevention, ignore messages which were posted by bot itself.
            # The bot_id attribute is collected from the Webex Teams API
            # at object instatiation.
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

                

                return data
        else: 
            return ('Wrong data format', 400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)