from flask import Flask, request, jsonify
import pg
import json

app = Flask(__name__)

@app.route("/sms")
def hello():
    return "Hello World!"

@app.route("/setrule", methods=['GET', 'POST'])
def sr():
    content = request.json

    try:
        id = content['id']
    except Keyerror:
        return json.dumps({'error': 'invalid id parameter'})
    # default to celsius
    try:
        scale = content['scale']
    except KeyError:
        scale = 1
    try:
        logic = content['logic']
    except Keyerror:
        return json.dumps({'error': 'invalid logic parameter'})

    print(id, scale, logic)

    res = pg.set_rule(id, scale, logic)
    return res

@app.route("/getrule", methods=['GET', 'POST'])
def gr():
    content = request.json

    try:
        id = content['id']
    except Keyerror:
        return json.dumps({'error': 'invalid id parameter'})

    print(id)

    res = pg.get_rule(id)
    return res

if __name__ == "__main__":
    app.run(debug=True)
