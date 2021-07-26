import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)
client = Client("AC0bddd51fb86522fdabd77a3bec1b6aaa",
                "42d41973aa30ac9a6309054c39006403")


def respond(message):
    response = MessagingResponse()
    print(response)
    response.message(message)
    return str(response)


@app.route('/message', methods=['POST'])
def reply():
    message = request.form.get('Body').lower()
    # if message:
    #     if message.isnumeric():
    #         return respond("""
    #     Perfect!! Your meal {} is to order

    #     Do you want agree any more

    #     (YES|NO)?
    #     """.format(message))

    #     elif message == "yes":
    #         return respond("What more do you agree to your meal (start with the sentence 'I Want'?")
    #     elif message == "no":
    #         return respond("Perfect!! You meal is completed! =)")
    #     elif message.startswith("i want"):
    #         return respond("Good decision! You meal is completed! =)")
    #     else:
    #         return respond("I'm sorry, i can not understand you ")
