import json
from twilio.rest import Client

with open("./constants.json") as f:
    data = f.read()
    account_phone = json.loads(data)['account_phone']
    account_sid = json.loads(data)['account_sid']
    auth_token = json.loads(data)['auth_token']

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="test body",
                     from_=account_phone,
                     to='+1512XXXXXXX'
                 )
# this is the UID of the outbound message
print(message.sid)
