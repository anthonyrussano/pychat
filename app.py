from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Store inputs in a global list
inputs = []


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", inputs=inputs)


@socketio.on("submit_input")
def handle_input(data):
    user_input = data["user_input"]
    inputs.append(user_input)
    emit("update_inputs", inputs, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001)
