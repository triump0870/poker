def poker(hands):
	"Return a list of wining hand: poker([hand,...]) => [hand,...]"
	return allmax(hands, key=hand_rank)
def allmax(iterable, key=None):
	"Return a list of all items equal to the max of the iterable."
	result, maxval = [],None
	key = key or (lambda x:x)
	for x in iterable:
		xval = key(x)
		if not result or xval > maxval:
			result, maxval = [x], xval
		elif xval == maxval:
			result.append(x)
	return result
def hand_rank(hand):
	"Return a value indicating the rank of a hand"
	ranks = card_ranks(hand)
	if straight(ranks) and flush(hand):
		return (8, max(ranks))
	elif kind(4,ranks):
		return (7,kind(4,ranks),kind(1,ranks))
	elif kind(3,ranks) and kind(2,ranks):
		return (6,kind(3,ranks),kind(2,ranks))
	elif flush(hand):
		return (5,ranks)
	elif straight(ranks):
		return(4,max(ranks))
	elif kind(3,ranks):
		return (3,kind(3,ranks),ranks)
	elif twopair(ranks):
		return (2,twopair(ranks),ranks)
	elif kind(2,ranks):
		return (1, kind(2,ranks),ranks)
	else:
		return (0,ranks)

def card_ranks(cards):
	"Return a list of the ranks, sorted with higher first"
	ranks = ['--23456789TJQKA'.index(r) for r,s in cards]
	ranks.sort(reverse=True)
	return [5,4,3,2,1] if ranks == [14,5,4,3,2] else ranks

def straight(ranks):
	"Return True if the ordered ranks a 5-card stright."
	return (max(ranks)-min(ranks)==4) and len(set(ranks))==5 #if straight then difference between the max ranked and min ranked card will be 4 and all the card will be different

def flush(hand):
	"Return True if all the card have the same suit."
	suits = [s for r,s in hand]
	return len(set(suits)) == 1 #if all the cards are in same card then the set length will be 1

def kind(n,ranks):
	"""Return the first rank that this hand has exactly n of.
	Return None if there is no n-of-a-kind in the hand."""
	for r in ranks:
		if ranks.count(r) == n: return r
	return None

def twopair(ranks):
	"""If there are two pair, return the two ranks as a tuple: (highest, lowest); otherwise return None."""
	pair = kind(2,ranks)
	lowpair = kind(2,list(reversed(ranks)))
	if pair and lowpair != pair:
		return (pair, lowpair)
	else:
		return None

def test():
	"Test cases for the functions in poker game"
	sf = "6C 7C 8C 9C TC".split() #straight and flush
	fk = "9D 9H 9S 9C 7D".split() #four-of-kind
	fh = "TD TC TH 7C 7D".split() #fullhouse
	tp = "5S 5D 9H 9C 6S".split() #twopair
	s1 = "AS 2S 3S 4S 5C".split() #A-5 straight
	s2 = "2C 3C 4C 5S 6S".split() #2-6 straight
	ah = "AS 2S 3S 4S 6C".split() #A high
	sh = "2S 3S 4S 6C 7D".split() #7 high
	fkranks = card_ranks(fk)
	tpranks = card_ranks(tp)
	assert kind(4,fkranks) == 9
	assert kind(3,fkranks) == None
	assert kind(2,fkranks) == None
	assert kind(1,fkranks) == 7
	assert twopair(fkranks) == None
	assert twopair(tpranks) == (9,5)
	assert straight([9,8,7,6,5]) == True
	assert straight([9,8,8,6,5]) == False
	assert flush(sf) == True
	assert flush(fk) == False
	assert card_ranks(sf) == [10,9,8,7,6]
	assert card_ranks(fk) == [9,9,9,9,7]
	assert card_ranks(fh) == [10,10,10,7,7]
	#assert poker([sf,fk,fh]) == sf
	#assert poker([fk,fh]) == fk
	#assert poker([fh,fh]) == fh
	assert hand_rank(sf) == (8,10)
	assert hand_rank(fk) == (7,9,7)
	assert hand_rank(fh) == (6,10,7)
	return "tests pass"


import random
def deal(numhands, n=5,deck=[r+s for r in "23456789TJQKA" for s in "CDHS"]):
	"""Shuffle the deck and deal out numhands n-card handa """
	random.shuffle(deck)
	return [deck[n*i:n*(i+1)] for i in range(numhands)]

def hand_percentage(n):
	"Sample a random hand and print a table of percentages for each of the hand."
	counts = [0] * 9
	hand_names = ['High cards', '1 pair', '2 pairs', '3-of-kind', 'Straight', 'Flush', 'Fullhouse', 'Four-of-kind', 'Straight-Flush']
	for i in xrange(n/10):
		for hand in deal(10):
			ranking = hand_rank(hand)[0]
			counts[ranking] += 1

	for i in reversed(xrange(9)):
		print "%14s: %6.4f %%"%(hand_names[i],100.*counts[i]/n)

hand_percentage(900000)