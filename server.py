from flask import Flask, session, render_template, redirect, request
app = Flask(__name__)
app.config['SECRET_KEY'] = 'woohoowhackamole!'

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
    players[name] = dict()
    session['name'] = name
    return redirect('/lobby/' + name)

# Lobby
@app.route('/lobby/<name>')
def lobby(name):
    return render_template('lobby.html', name=name)

# Answer
@app.route('/answer/<name>')
def answer(name):
	return render_template('answer.html', name=name)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form["username"]
    print (request.form)
    players[name]["responses"] = (request.form["answer1"],request.form["answer2"])
    print ("answer 1: " + players[name]["responses"][0])
    print ("answer 2: " + players[name]["responses"][1])
    return redirect('/vote')

# Vote for the best responses
# once this game expands we can try to make multiple lobbies/multiple games at once
@app.route('/vote', methods=['GET'])
def vote():
	return render_template('vote.html')

# Display scores
@app.route('/scores', methods=['GET'])
def scores():
	return render_template('scores.html')

app.run(host='127.0.0.1', port=8000)
