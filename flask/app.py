from flask import Flask
from pg import connect
from pg import foo

app = Flask(__name__)

@app.route("/sms")
def hello():
    return "Hello World!"

@app.route("/pg")
def pgget():
    out = connect()
    return out

@app.route("/pgtest")
def pgtest():
    out2 = foo()
    return out2

if __name__ == "__main__":
    app.run(debug=True)
