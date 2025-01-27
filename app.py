from flask import Flask, render_template, request
from flask_socketio import SocketIO
import model
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("splash.html")

@app.route("/begin")
def get_heartrate():
    return render_template("index.html")

@socketio.on('message')
def echo_socket(message):
    data = json.loads(message)
    signals = model.parse_RGB(data)
    socketio.send(signals)

if __name__ == "__main__":
    socketio.run(app, debug=True)
