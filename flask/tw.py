import json
from twilio.rest import Client

def send_sms(message):
    """
    Sends sms with optional body message via twilio api
    """
    with open("./constants.json") as f:
        data = f.read()
        account_phone = json.loads(data)['twilio']['account_phone']
        account_sid = json.loads(data)['twilio']['account_sid']
        auth_token = json.loads(data)['twilio']['auth_token']
        tgt_phone = json.loads(data)['twilio']['tgt_phone']

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=message,
                         from_=account_phone,
                         to=tgt_phone
                     )
    # this is the UID of the outbound message
    print(message.sid)
