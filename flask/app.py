from flask import Flask, request, jsonify, Response
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
        # if greater than logic, must have templ
        if logic == 0:
            try:
                templ = content['templ']
                temph = None
            except Keyerror:
                return json.dumps({'error': 'low temp needed for greater than logic'})
        # if less than logic, must have temph
        if logic == 1:
            try:
                temph = content['temph']
                templ = None
            except Keyerror:
                return json.dumps({'error': 'high temp needed for less than logic'})
        # if OOB logic, must have both low and high temp limits
        if logic == 2:
            try:
                templ = content['templ']
                templ = content['temph']
            except Keyerror:
                return json.dumps({'error': 'both low and high temp needed for OOB logic'})
    except Keyerror:
        return json.dumps({'error': 'invalid logic parameter'})

    print(id, scale, logic, templ, temph)

    res = pg.set_rule(id, logic, templ, temph, scale)
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
