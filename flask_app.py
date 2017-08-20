
import requests
import json
from flask import Flask, request
import apiai
from config import Config
from helpers import classify, model, response

import nltk
from nltk.stem.lancaster import LancasterStemmer
# stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

# FB messenger credentials
ACCESS_TOKEN=Config.ACCESS_TOKEN
# api.ai credentials
CLIENT_ACCESS_TOKEN=Config.CLIENT_ACCESS_TOKEN

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

# create a data structure to hold user context


@app.route('/', methods=['GET'])
def verify():

    # our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return 'Hello World (from Flask!)', 200

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
        # "message": {"text": 'mulle meeldib vorstu'}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']

    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = message

    # get response from API.ai
    # api_response = req.getresponse()
    api_response = response(message)
    reply(sender, api_response)
    # responsestr = api_response.read().decode('utf-8')
    # response_obj = json.loads(responsestr)
    # if 'result' in response_obj:
    #     response = response_obj["result"]["fulfillment"]["speech"]
    #     reply(sender, response)

    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
