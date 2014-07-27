#! /usr/bin/env python

import random

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    iterable.sort(key=key,reverse=True)
    result = [iterable[0]]
    maxValue = key(iterable[0]) if key else iterable[0]
    for value in iterable[1:]:
        v = key(value) if key else value
        if v == maxValue: result.append(value)
        else: break
    return result

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has exactly n-of-a-kind of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    "If there are two pair here, return the two ranks of the two pairs, else None."
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def hand_rank_alt(hand):
    "Return a value indicating how high the hand ranks."
    # count is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1) ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):   # Ace low straight
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return (9 if (5,) == counts else
            8 if straight and flush else
            7 if (4, 1) == counts else
            6 if (3, 2) == counts else
            5 if flush else
            4 if straight else
            3 if (3, 1, 1) == counts else
            2 if (2, 2, 1) == counts else
            1 if (2, 1, 1, 1) == counts else
            0), ranks

count_rankings = {(5,): 10, (4, 1): 7, (3, 2): 6, (3, 1, 1): 3, (2, 2, 1): 2,
                  (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}

def hand_rank_table(hand):
    "Return a value indicating how high the hand ranks."
    # count is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 9 7' => counts = (3, 1, 1) ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):   # Ace low straight
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r,s in hand])) == 1
    return max(count_rankings[counts], 4*straight + 5*flush), ranks

def group(items):
    "Return a list of [(count, x), ...], highest count first, then highest x first"
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse = True)

def unzip(iterable):
    "Return a list of tuples from a list of tuples : e.g. [(2, 9), (2, 7)] => [(2, 2), (9, 7)]"
    return zip(*iterable)

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def deal(numhands, n=5, deck=mydeck):
    random.shuffle(mydeck)
    return [mydeck[n*i:n*(i+1)] for i in range(numhands)]

hand_names = ["Straight flush", "Four of a kind", "Full house", "Flush", "Straight",
              "Three of a kind", "Two pair", "One pair", "High card"]

def hand_percentages(n=700*1000):
    counts = [0]*9
    for i in xrange(n/10):
        for hand in deal(10):
            ranking = hand_rank_alt(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print "%15s: %6.3f %%" % (hand_names[-(i+1)], 100.*counts[i]/n)

def test():
    "Test cases for the functions in poker program."
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    tp = "5D 2C 2H 9H 5C".split() # Two Pair

    # Testing allmax
    assert allmax([2,4,7,5,1]) == [7]
    assert allmax([2,4,7,5,7]) == [7,7]
    assert allmax([2]) == [2]
    assert allmax([0,0,0]) == [0,0,0]

    # Testing card_ranks
    assert card_ranks(sf1) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    # Testing flush
    assert flush([]) == False
    assert flush(sf1) == True
    assert flush(fh) == False

    # Testing straight
    assert straight(card_ranks(sf1)) == True
    assert straight(card_ranks(fk)) == False

    # Testing kind
    assert kind(3, card_ranks(sf1)) == None
    assert kind(4, card_ranks(fk)) == 9

    # Tesing two pair
    assert two_pair(card_ranks(sf1)) == None
    assert two_pair(card_ranks(tp)) == (5,2)

    # Testing group
    assert group([2,3,4,6,2,1,9]) == [(2,2),(1,9),(1,6),(1,4),(1,3),(1,1)]
    assert group([8,8,8,8]) == [(4,8)]
    assert group([2,6,1]) == [(1,6),(1,2),(1,1)]

    # Testing unzip
    assert unzip([(2,2),(1,9),(1,6),(1,4),(1,3),(1,1)]) == [(2,1,1,1,1,1),(2,9,6,4,3,1)]
    assert unzip([(1,6),(1,2),(1,1)]) == [(1,1,1),(6,2,1)]
    assert unzip([(2, 9), (2, 7)]) == [(2, 2), (9, 7)]

    # Testing hand rank
    assert hand_rank(sf1) == (8,10)
    assert hand_rank(fk) == (7,9,7)
    assert hand_rank(fh) == (6,10,7)

    # Testing hand rank alt
    assert hand_rank_alt(sf1) == (8, (10,9,8,7,6))
    assert hand_rank_alt(fk) == (7,(9,7))
    assert hand_rank_alt(fh) == (6,(10,7))

    # Testing hand rank table
    assert hand_rank_table(sf1) == (9, (10,9,8,7,6))
    assert hand_rank_table(fk) == (7,(9,7))
    assert hand_rank_table(fh) == (6,(10,7))

    # Testing poker
    assert poker([sf1, fk, fh]) == [sf1]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([fh]) == [fh]
    assert poker([sf2] + 99*[fh]) == [sf2]
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]

    return 'tests pass'
print test()
hand_percentages()