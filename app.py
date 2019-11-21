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
                if 'text' in message['message']:
                    response = Text(text='This is an example text message.')
                    send_message(recipient_id, response)
                    # if 'image' in msg:
                    #     response = Image(url='https://unsplash.it/300/200/?random')
                    #     send_message(recipient_id, response)
                    # if 'video' in msg:
                    #     response = Video(url='http://techslides.com/demos/sample-videos/small.mp4')
                    #     send_message(recipient_id, response)
    return "Message Processed"

# def process_message(message):
#     app.logger.debug('Message received: {}'.format(message))
#
#     if 'attachments' in message['message']:
#
#
#     if 'text' in message['message']:
#         msg = message['message']['text'].lower()
#         response = Text(text='Sorry didn\'t understand that: {}'.format(msg))
#
#         if 'quick replies' in msg:
#             qr1 = quick_replies.QuickReply(title='Location', content_type='location')
#             qr2 = quick_replies.QuickReply(title='Payload', payload='QUICK_REPLY_PAYLOAD')
#             qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
#             response = Text(text='This is an example text message.', quick_replies=qrs)
#         if 'payload' in msg:
#             txt = 'User clicked {}, button payload is {}'.format(
#                 msg,
#                 message['message']['quick_reply']['payload']
#             )
#             response = Text(text=txt)
#         if 'webview-compact' in msg:
#             btn = get_button(ratio='compact')
#             elem = get_element(btn)
#             response = GenericTemplate(elements=[elem])
#         if 'webview-tall' in msg:
#             btn = get_button(ratio='tall')
#             elem = get_element(btn)
#             response = GenericTemplate(elements=[elem])
#         if 'webview-full' in msg:
#             btn = get_button(ratio='full')
#             elem = get_element(btn)
#             response = GenericTemplate(elements=[elem])
#
#         return response.to_dict()


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

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run()
