from flask import Flask
import pg

app = Flask(__name__)

@app.route("/sms")
def hello():
    return "Hello World!"

@app.route("/getver")
def pgtest():
    out2 = pg.get_ver()
    return out2

@app.route("/setrule")
def sr():
    out3 = pg.set_rule('a', 1, 1)
    return out3

if __name__ == "__main__":
    app.run(debug=True)
