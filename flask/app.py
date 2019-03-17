from flask import Flask, request, jsonify, Response
import pg
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def id():
    res = pg.input_data(request)
    return res

@app.route("/setrule", methods=['POST'])
def sr():
    res = pg.set_rule(request)
    return res

@app.route("/getrule", methods=['GET'])
def gr():
    res = pg.get_rule(request)
    return res

if __name__ == "__main__":
    app.run(debug=True)
