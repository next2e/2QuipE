import itertools
import random

def makeSets(num_players):
    q = [a for a in range(num_players)]
    rawsets = list(itertools.combinations(q,2))
    
    # scramble the sets for randomness
    sets = []
    n = len(rawsets)
    for i in range((num_players*(num_players-1))//2):
        j = random.randint(0,n-1)
        sets.append(rawsets[j])
        rawsets.remove(rawsets[j])
        n -= 1
    
    return sets, q

def countAllGood(counts, num_players):
    for i in range(num_players):
        if counts.count(i) % 2 == 1:
            return True

    return False

def generatePairs(num_players):
    sets, q = makeSets(num_players)
    # create a list containing two copies of each question
    counts = q+q
    generated = []
    repeated = 0

    while (len(generated) != len(q) and repeated < 2):
        repeated += 1
        #print ("Going again...")
        for index,s in enumerate(sets):
            # if this combination still is left in counts, remove
            # it so that we never use a question more than twice
            if s[0] in counts and s[1] in counts:
                counts.remove(s[0])
                counts.remove(s[1])
                if (countAllGood(counts, num_players) or len(counts) == 0):
                    generated.append(s)
                else: #refuse - closed loops are bad, could cause cases of 1 problem never being used
                    counts.append(s[0])
                    counts.append(s[1])

    if (repeated == 2 and len(generated) != len(q)): generated.append(tuple(counts)) # counts will have 1 pair remaining - a repeat
    return generated

def load_questions(n): 
    with open('questions.txt') as f:
        return random.sample(f.read().split('\n')[:-1], n)
        
def assign_questions(players):
    num = len(players)
    q = load_questions(num)
    p = generatePairs(num)
    # assign questions to players
    for i,name in enumerate(players):
        players[name]['questions'] = (q[p[i][0]], q[p[i][1]])
    # assign players to questions
    # after answers are assigned to each question,
    # this makes displaying answers on vote.html easier
    for name in players:
        for i in range(2):
            if players[name]['questions'][i] in questions:
                questions[players[name]['questions'][i]].append(name)
            else:
                questions[players[name]['questions'][i]] = [name]

    return players, questions

