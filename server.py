from flask import Flask, session, render_template, redirect, request
app = Flask(__name__)

# global variables
global players
players = {}

# Home page
@app.route('/')
def main():
    return render_template('index.html', players =
        (', '.join(list(players.keys())) if players else "Nobody"))

# Join a game
@app.route('/join', methods=['POST'])
def join():
    name = request.form["username"]
    players[name] = None
    session['name'] = name
    return redirect('/lobby')

app.run(host='127.0.0.1', port=8000)
