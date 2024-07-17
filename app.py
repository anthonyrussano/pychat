from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)


# Database setup
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  message TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"""
    )
    conn.commit()
    conn.close()


def get_messages():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("SELECT message FROM messages ORDER BY timestamp")
    messages = [row[0] for row in c.fetchall()]
    conn.close()
    return messages


def add_message(message):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    messages = get_messages()
    return render_template("index.html", inputs=messages)


@socketio.on("submit_input")
def handle_input(data):
    user_input = data["user_input"]
    add_message(user_input)
    messages = get_messages()
    emit("update_inputs", messages, broadcast=True)


if __name__ == "__main__":
    init_db()
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
