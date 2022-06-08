# z5169989
# Duy Thong Trinh

from flask import Flask, jsonify, abort, request, g
import json
import requests
import random
import re
import os
import sys
import copy
from flask_cors import CORS, cross_origin
from wit import Wit

from recom import make_recommendation
from pop import popular_rec


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
client = Wit("LPY6W75RGEOTJ42BD2TME53VEJJMVZMQ")

USERNAME = ""


@app.route('/')
@cross_origin()
def index():
    msg = request.args.get("message")
    print(msg)
    # newmsg = copy.copy(msg)
    resp = client.message(msg)
    print(resp)
    # The chatbot should be able to respond to basic greetings
    if resp['intents'][0]['name'] == 'Greeting':
        list_of_rep = ['Hi! Can I ask what is your name?',
        'Hello! Can you please tell me your name?',
        'Good day! How about you tell me your name?',
        'Greetings! What can I call you?']
        reply = random.choice(list_of_rep)
        reply = [reply]
        return jsonify({"type": "mess1", "message": reply})

    elif resp['intents'][0]['name'] == 'AskName':
        global USERNAME
        username = resp['entities']['PersonName:PersonName'][0]['body']
        USERNAME = username
        rep = "Hello {}. What can I do for you today?".format(USERNAME)
        rep = [rep]
        return jsonify({"type": "mess1", "message": rep})

    elif resp['intents'][0]['name'] == 'UsrInfRec':
        rep = "Sure. Please type in movie's genre, name of actors/directors, keywords, all seperate by comma"
        rep = [rep]
        return jsonify({"type": "mess1", "message": rep})

    elif resp['intents'][0]['name'] == 'UsrPref':
        newmsg = copy.copy(msg)
        newmsg = newmsg.split(",")
        newmsg1 = [x.strip(" ") for x in newmsg]
        newmsg2 = [x.replace(" ", "") for x in newmsg1]
        query = ' '.join([str(elem) for elem in newmsg2])
        print(query)
        response = make_recommendation(query)
        print(response)
        new_list = []
        for i in response:
            temp = '++++'.join([str(elem) for elem in i])
            new_list.append(temp)
        
        res1 = '****'.join([str(elem) for elem in new_list])

        return jsonify({"type": "mess2", "message": [res1]})

    elif resp['intents'][0]['name'] == 'PopRec':
        response = popular_rec()
        print(response)
        new_list = []
        for i in response:
            temp = '++++'.join([str(elem) for elem in i])
            new_list.append(temp)
        
        res1 = '****'.join([str(elem) for elem in new_list])

        return jsonify({"type": "mess2", "message": [res1]})
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
