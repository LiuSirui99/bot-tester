import os
from pymessenger.bot import Bot
from flask import Flask, request
from fbmessenger import BaseMessenger
from fbmessenger.templates import GenericTemplate
from fbmessenger.elements import Text, Button, Element
from fbmessenger import quick_replies
from fbmessenger.attachments import Image, Video
from fbmessenger.thread_settings import (
    GreetingText,
    GetStartedButton,
    PersistentMenuItem,
    PersistentMenu,
    MessengerProfile,
)
FB_PAGE_TOKEN = 'EAAhBgAvgBxgBAOMZB8zBAyaAHGLTusOH1yILf3ZCYq3Cykuzh4GlxZCQR9LonOh2qfmSUp2aBfBhZCalH14k5kifzUq7ItFI7seiNUu6irZCgZBhx6XqQtXIH1Op8CHYZBaPpZB3yedZA3VlqEZBzMe6YwZAMNN1PUrZAghhorTs5wtqVAZDZD'
FB_VERIFY_TOKEN = 'test_token'

def get_button(ratio):
    return Button(
        button_type='web_url',
        title='facebook {}'.format(ratio),
        url='https://facebook.com/',
        webview_height_ratio=ratio,
    )


def get_element(btn):
    return Element(
        title='Testing template',
        item_url='http://facebook.com',
        image_url='http://placehold.it/300x300',
        subtitle='Subtitle',
        buttons=[btn]
    )

def receive_message():
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
            #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    msg = message['message']['text'].lower()
                    response = Text(text='Sorry didn\'t understand that: {}'.format(msg))
                    if 'text' in msg:
                        response = Text(text='This is an example text message.')
                    if 'image' in msg:
                        response = Image(url='https://unsplash.it/300/200/?random')
                    if 'video' in msg:
                        response = Video(url='http://techslides.com/demos/sample-videos/small.mp4')
                    return response.to_dict()
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    if message['message']['attachments'][0]['type'] == 'location':
                        app.logger.debug('Location received')
                        response = Text(text='{}: lat: {}, long: {}'.format(
                        message['message']['attachments'][0]['title'],
                        message['message']['attachments'][0]['payload']['coordinates']['lat'],
                        message['message']['attachments'][0]['payload']['coordinates']['long']
                        ))
                        return response.to_dict()

    return "Message Processed"


app = Flask(__name__)
app.debug = True
# messenger = Messenger(FB_PAGE_TOKEN)
bot = Bot(FB_PAGE_TOKEN)
@app.route("/", methods=['GET', 'POST'])
# @app.route('/webhook', methods=['GET', 'POST'])
def verify_fb_token():
    if request.args.get('hub.verify_token') == FB_VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return 'Invalid verification token'



if __name__ == '__main__':
    app.run()
