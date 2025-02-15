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

    # Check for winner in rows, columns and diagonals 
    for i in range(3):
        if session["board"][i][0] == session["board"][i][1] == session["board"][i][2] is not None:
            return redirect(url_for("winner", winner=session["board"][i][0]))
        if session["board"][0][i] == session["board"][1][i] == session["board"][2][i] is not None:
            return redirect(url_for("winner", winner=session["board"][0][i]))
    
    # Diagonals 
    if session["board"][0][2] == session["board"][1][1] == session["board"][2][0] is not None:
        return redirect(url_for("winner", winner=session["board"][0][2]))
    if session["board"][0][0] == session["board"][1][1] == session["board"][2][2] is not None:
        return redirect(url_for("winner", winner=session["board"][0][0]))       

    # Draw
    for row in session["board"]:
        for cell in row:
            if cell is None:
                return render_template("game.html", game=session["board"], turn=session["turn"])
        return redirect(url_for("winner", winner="Draw"))
            
    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

@app.route("/move")
def undo_move():
    # Undo the last move
    for i in range(3):
        for j in range(3):
            print(session["board"][i])
            if session["board"][i][j] is not None:
                session["board"][i][j] = None
                session["turn"] = "X" if session["turn"] == "O" else "O"
                return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/winner/<string:winner>")
def winner(winner):
    if winner == 'Draw':
        return render_template("winner.html", draw=winner)
    else:
        return render_template("winner.html", winner=winner)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides a PORT
    app.run(debug=True, host="0.0.0.0", port=port)