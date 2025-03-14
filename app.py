#Python libraries that we need to import for our bot
import os
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os
app = Flask(__name__)
ACCESS_TOKEN = 'EAAhBgAvgBxgBAOMZB8zBAyaAHGLTusOH1yILf3ZCYq3Cykuzh4GlxZCQR9LonOh2qfmSUp2aBfBhZCalH14k5kifzUq7ItFI7seiNUu6irZCgZBhx6XqQtXIH1Op8CHYZBaPpZB3yedZA3VlqEZBzMe6YwZAMNN1PUrZAghhorTs5wtqVAZDZD'
VERIFY_TOKEN = 'test_token'
bot = Bot (ACCESS_TOKEN)

def send_get_started(bot,recipient_id):
    button = {
        "get_started":{
            "payload" : "first_coming"
        }
    }

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if 'text' in message['message']:
                        msg = message['message']['text']
                        response = 'We are happy to have you here:) \n \n Try sending me one of these messages: ''Chat, Selfie, Upload id, Rating'
                        if 'Hello' in msg:
                            response = 'Hey, We are happy to have you here:) \n \n Try sending me one of these messages: ''Chat, Selfie, Upload id, Rating'''
                        if 'Selfie' in msg:
                            response = 'Please send us your recent clear selfie for authentication here: http://127.0.0.1:5000'
                        if 'selfie' in msg:
                            response = 'Please send us your recent clear selfie for authentication here http://127.0.0.1:5000.'
                        if 'Upload id' in msg:
                            response = 'Please send us your recent clear identification document for authentication here http://127.0.0.1:5000.'
                        if 'upload' in msg:
                            response = 'Do you mean uploading selfie or identification card for authentification process?\n  \n Try sending me one of these messages: ''Chat, Selfie, Upload id, Rating '
                        if 'Chat' in msg:
                            response = get_message()
                        if 'Rating' in msg:
                            response = 'Please rate us from 1-5. \n \n  We are always working on the best service :)'
                        send_message(recipient_id, response)

                    #if user sends us a GIF, photo,video, or any other non-text item
                    if 'attachments' in message['message']:
                        response_sent_nontext = 'Picture well received, thank you :)' + get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
