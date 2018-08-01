class ScoreCard:
	# card structure
	# name1: (number of people who voted for said person)
	# name2: (number of people who voted for said person)
	# a new scoreCard is made for every question

	def __init__(self, question, names):
		self.card[names[0]] = 0
		self.card[names[1]] = 0
		self.question = question

	def submitVote(name):
		self.card[name] += 1

	def getCard():
		return self.card

class TotalScore:
	# keeps track of running number of points across all players
	# contains a list of ScoreCards

	def __init__(self):
		self.scoreCards = [] # list of ScoreCards
