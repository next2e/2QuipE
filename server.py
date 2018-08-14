from flask import Flask, session, render_template, redirect, request, jsonify
from werkzeug.contrib.cache import SimpleCache
import os
import question
os.system("python question.py")

cache = SimpleCache()
cache.set('started', False) # has the game started
cache.set('players', {}) # dictionary with players as keys
cache.set('questions', {}) # dictionary with questions as keys
cache.set('areQuestionsOrdered', False) # have the questions been ordered?
cache.set('orderedQuestions', []) # the list of ordered questions

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
	players, questions = question.assignQuestions(players)
	cache.set('players', players) # each individual player then populates answer.html with their own questions
	cache.set('questions', questions) # questions matched to players
	return 'ok' #required to return something

# get questions assigned to each player
@app.route('/answer/get_questions', methods=['GET'])
def getQuestions():
	name = request.args.get('name')
	players = cache.get('players')
	return jsonify(players[name]['questions'])

# Answer
@app.route('/answer/<name>')
def answer(name):
	return render_template('answer.html', name=name)

@app.route('/submit', methods=['POST'])
def submit():
	name = request.form["name"]
	players = cache.get('players')
	questions = cache.get('questions')
	playerQuestions = players[name]['questions']

	players[name]["responses"] = (request.form["answer1"],request.form["answer2"])
	print (questions[playerQuestions[0]]['names'])
	print (name)
	for i in range(2):
		if questions[playerQuestions[i]]['names'].index(name) == 1: # is 1
			# populate second element in responses
			questions[playerQuestions[i]]['responses'][1] = request.form["answer"+str(i+1)]
		else: # is 0
			questions[playerQuestions[i]]['responses'][0] = request.form["answer"+str(i+1)]
	
	print ("answer 1: " + players[name]["responses"][0])
	print ("answer 2: " + players[name]["responses"][1])
	print ("new questions dictionary!")
	print (questions)
	cache.set('players', players)
	cache.set('questions', questions)
	return redirect('/vote')
	# return 'ok'

# Vote for the best responses
# once this game expands we can try to make multiple lobbies/multiple games at once
@app.route('/vote', methods=['GET'])
def vote():
	isOrdered = cache.get('areQuestionsOrdered')
	if not(isOrdered):
		questions = cache.get('questions')
		cache.set('orderedQuestions', question.orderQuestionsForAnswers(questions))
		cache.set('areQuestionsOrdered', True)
		print ("Yee Haw")

	return render_template('vote.html')

# Display scores
@app.route('/scores', methods=['GET'])
def scores():
	return render_template('scores.html')

app.run(host='127.0.0.1', port=8000)
