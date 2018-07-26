from flask import Flask, session, render_template, redirect, request, jsonify
from werkzeug.contrib.cache import SimpleCache
import os
import question
os.system("python question.py")

cache = SimpleCache()
cache.set('started', False)
cache.set('players', {})

app = Flask(__name__)
app.config['SECRET_KEY'] = 'woohoowhackamole!'

# Home page
@app.route('/')
def main():
    players = cache.get('players')
    return render_template('index.html', players =
        (', '.join(list(players.keys())) if players else "Nobody"))

# Join a game
@app.route('/join', methods=['POST'])
def join():
    name = request.form["username"]
    players = cache.get('players')
    players[name] = dict()
    cache.set('players', players)

    session['name'] = name
    return redirect('/lobby/' + name)

# Lobby
@app.route('/lobby/<name>')
def lobby(name):
    return render_template('lobby.html', name=name)

# Check started
@app.route('/lobby/check_started', methods=['GET'])
def checkStarted():
    data = dict()
    name = session['name']

    data['name'] = name
    data['start'] = cache.get('started')
    players = cache.get('players')
    data["players"] = (', '.join(list(players.keys())) if players else "Nobody")
    return jsonify(data)

# Check started but someone pressed the button
@app.route('/lobby/check_started', methods=['POST'])
def start():
    cache.set('started', True)

    # then assign questions to players
    players = cache.get('players')
    players = question.assign_questions(players)
    cache.set('players', players) # each individual player then populates answer.html with their own questions
    return 'ok' #required to return something

# get questions assigned to each player
@app.route('/answer/get_questions', methods=['GET'])
def getQuestions():
    name = session['name']
    players = cache.get('players')
    return jsonify(players[name]['questions'])

# Answer
@app.route('/answer/<name>')
def answer(name):
    return render_template('answer.html', name=name)

@app.route('/submit', methods=['POST'])
def submit():
    name = session['name']
    players = cache.get('players')
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
