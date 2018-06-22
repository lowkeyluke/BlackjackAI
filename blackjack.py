"""Blackjack classes/objects, and methods.
Imported into each file that uses the deck"""

import random

class Card(object):
    def __init__(self, rank, value, suit):
        self.rank = rank
        self.value = value
        self.suit = suit

    def printCard(self):
        return self.rank, self.suit

    def getcardValue(self):
        return self.value

    def setcardValue(self, v):
        self.value = v

class Deck(object):
    def __init__(self):
        self.cards = []
        self.buildDeck()

    def buildDeck(self):
        for s in ["♠", "♣", "♦", "♥"]:
            for r in range(2,15):
                v = r
                if r == 11:
                    r = "J"
                    v = 10
                if r == 12:
                    r = "Q"
                    v = 10
                if r == 13:
                    r = "K"
                    v = 10
                if r == 14:
                    r = "A"
                    v = 11
                self.cards.append(Card(r, v, s))

    def printDeck(self):
        for c in self.cards:
            c.printCard()

    def shuffle(self):
        for i in range(0, len(self.cards)):
            randomnum = random.randint(0, i)
            self.cards[i], self.cards[randomnum] = self.cards[randomnum], self.cards[i]

    def draw(self):
        return self.cards.pop()

class Player(object):
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.splithand = []
        self.chips = 1000
        self.pot = 0
        self.count = 0

    def draw(self, split=False):
        if split:
            self.splithand.append(deck1.draw())
            # count cards
            card = self.hand[-1]
            if card.value >= 10:
                self.count += 1
        else:
            self.hand.append(deck1.draw())
            # count cards
            card = self.hand[-1]
            if card.value >= 10:
                self.count += 1

    def showHand(self, split=False):
        if split:
            print("Split")
            for c in self.splithand:
                c.printCard()
        elif not split:
            # print(self.name + ":")
            hand = ""
            for c in self.hand:
                hand += str(c.printCard())
            return hand

    def handValue(self):
        totalvalue = 0
        for v in self.hand:
            totalvalue += v.getcardValue()
        return totalvalue

    def blackjack(self):
        bj = False
        if self.handValue() == 21 and len(self.hand) == 2:
            bj = True
        return bj

    def bet(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            self.pot = self.pot + (amount*2)

    def insurance(self, amount):
        price = amount/2
        self.chips -= price

    def collectPot(self, bj=False, push=False, split=False):
        if bj:
            if split:
                self.chips += (self.pot *1.25)/2
                self.pot = self.pot/2
            elif not split:
                self.chips += self.pot * 1.25
                self.pot = 0
        if push:
            if split:
                self.chips += self.pot/4
                self.pot = self.pot/2
            elif not split:
                self.chips += self.pot/2
                self.pot = 0
        if split:
            self.chips += self.pot/2
            self.pot = self.pot/2
        elif not split:
            self.chips += self.pot
            self.pot = 0

class Dealer(Player):
    def __init__(self, name):
        super(Dealer, self).__init__(name)

def saveScore(name, chips):
    HSfile = open("hiscores.txt", "a")
    HSfile.write("\n")
    HSfile.write(name)
    HSfile.write(":")
    HSfile.write(str(chips))
    HSfile.close()

def printScores():
    print("High Scores:")
    HSfile = open("hiscores.txt", "r")
    score = HSfile.read()
    HSfile.close()
    print(score)

def saveChips(name, chips):
    nametxt = name + ".txt"
    SCfile = open(nametxt, "w+")
    SCfile.write(str(chips))
    SCfile.close()
    print("Chips:", chips)

#scores2 = [("x", 0), ("x", 0), ("x", 0)]
#scores = [0,0,0]
#for rank in scores:
#    if player1.chips-1000 > rank:
#        scores[rank] = player1.chips-1000
#print(scores)

def exitoption(code):
    if code == 69:
        player1.chips = int(player1.chips)
        if player1.chips > 1000:
            print("You earned", player1.chips-1000, "chips!", "Good job,", name+"!")
            saveScore(name, str(player1.chips-1000))
            printScores()
        if player1.chips == 1000:
            print("You broke even.")
        if player1.chips <= 0:
            print("You went bankrupt!! Sorry bud.")
        elif player1.chips < 1000:
            print("You lost", 1000-player1.chips, "chips. Better luck next time!")
        printit = int(input("1 for high scores"))
        if printit > 0:
            printScores()

    if code == 70:
        player1.chips = int(player1.chips)
        saveChips(name, player1.chips)

deck1 = Deck()