import os

from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    session["turn"] = "X" if session["turn"] == "O" else "O"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

@app.route("/computer")
def computer(game, turn):
    # AI to make its turn
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides a PORT
    app.run(debug=True, host="0.0.0.0", port=port)