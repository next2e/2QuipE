class ScoreCard:
	# card structure
	# name1: (number of people who voted for said person)
	# name2: (number of people who voted for said person)
	# a new scoreCard is made for every question

	def __init__(self, question, names):
		self.card = dict()
		self.card[names[0]] = 0
		self.card[names[1]] = 0
		self.question = question

	def getNames(self):
		tortn = []
		for n in self.card:
			tortn.append(n)
		return tortn

	def getVotes(self, name):
		return self.card[name]

	def submitVote(self,name):
		self.card[name] += 1

	def __str__(self):
		tortn = "Prompt: " + self.question + "\nVotes per person: \n"
		for k in self.card:
			tortn += k + ": " + str(self.card[k]) + "\n" 
		return tortn

class TotalScore:
	# keeps track of running number of points across all players
	# contains a list of ScoreCards
	# scoreCard only added to TotalScore when voting is complete

	pointsPerVote = 100
	pointsPerSweep = 200

	def __init__(self, names):
		self.scoreCards = [] # list of ScoreCards
		self.names = dict() # make dict of names from list of names
		for n in names:
			self.names[n] = 0

	def getTotalScore(self):
		return self.names

	def getCards(self):
		return self.scoreCards

	def getCardByQuestion(self, question):
		for c in scoreCards:
			if c.question == question:
				return c.card
		return dict() # no card corresponding to question

	def addScoreCard(self,card):
		self.scoreCards.append(card)
		names = card.getNames()
		if card.getVotes(names[0]) == 0:
			self.names[names[1]] += 200
		elif card.getVotes(names[1]) == 0:
			self.names[names[0]] += 200
		self.names[names[0]] += card.getVotes(names[0])*100
		self.names[names[1]] += card.getVotes(names[1])*100

