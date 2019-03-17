from flask import Flask, request, jsonify, Response
import pg
import json

app = Flask(__name__)

@app.route("/sms")
def hello():
    return "Hello World!"

@app.route("/setrule", methods=['GET', 'POST'])
def sr():
    res = pg.set_rule(request)
    return res

@app.route("/getrule", methods=['GET', 'POST'])
def gr():
    content = request.json

    try:
        id = content['id']
    except Keyerror:
        return Response(
            json.dumps({'error': 'invalid id parameter'}),
            status=400,
            mimetype='application/json'
        )

    print(id)

    res = pg.get_rule(id)
    if res is not None:
        return Response(
            res,
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            json.dumps({'error': 'no rules for specified sensor'}),
            status=204,
            mimetype='application/json'
        )

if __name__ == "__main__":
    app.run(debug=True)
