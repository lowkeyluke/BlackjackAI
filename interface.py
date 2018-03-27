"""Game with GUI and neural net with 3 layers (1 hidden layer).
NOT OPTIMAL. SEE LAYER4.py"""

from tkinter import *
from blackjack import *
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np

'''Set up window'''

window = Tk()
window.title("lowkeyluke's BJ")
window.geometry("300x300")

# Menu Bar
menu = Menu()
window.config(menu=menu)

'''HIGH SCORES'''
def printScores():
    print("High Scores:")
    HSfile = open("hiscores.txt", "r")
    score = HSfile.read()
    HSfile.close()
    print(score)
    '''Try to implement high scores to GUI'''
    # hiscore = Label(text=printScores)
    # hiscore.grid(column=5, row=0)

#  File tab
file = Menu(menu)
file.add_command(label="High Scores", command=printScores)
file.add_command(label="Save", command=exit)
file.add_command(label="Exit", command=exit)
menu.add_cascade(label="File", menu=file)

# Edit tab
edit = Menu(menu)
edit.add_command(label="Undo")
menu.add_cascade(label="Edit", menu=edit)

# Click submit button to submit name
def submitName():
    name = entry.get()
    # remove submit button and textbox
    submit.grid_remove()
    textbox.grid_remove()
    return name

# Click submit button to submit bet
def submitBet():
    betamount = entry.get()
    submit2.grid_remove()
    textbox.grid_remove()
    return betamount

submit = Button(text="Submit Name", command=submitName)
# submit.grid(column=1, row=1)
submit2 = Button(text="Submit", command=submitBet)
# submit2.grid(column=2, row=1)

def hit():
    player1.draw()
    label3.configure(text="" + str(player1.name) + ": " + str(player1.showHand()) + ": " + str(player1.handValue()))

'''Set up game'''
# Labels
label = Label(text="LowkeyLuke's BlackJack")
label2 = Label(text="...")
label3 = Label(text="...")
label4 = Label(text="...")
label.grid(column=0, row=0)
label2.grid(column=0, row=1)
label3.grid(column=0, row=2)
label4.grid(column=0, row=3)

# Textbox entry widget
entry = StringVar()
textbox = Entry(width=12, textvariable=entry)
textbox.grid(column=1, row=0)
textbox.focus()  # Place cursor in textbox

name = simpledialog.askstring("Name", "Let's play BlackJack! What's your name?")
player1 = Player(name)
dealer1 = Dealer("THE DEALER")

deck1.shuffle()
discardpile = []

'''Create input data array and output data array for Neural Network'''
# STATIC AI
X = np.array([[10,10],[20,5],[20,10],[5,5]])  # append [player total, dealer upcard] to array at start of each hand
Y = np.array([[1],[0],[0],[1]])  # if hit==true and collectPot==true, append 1. if hit==true and collectPot==false, append 0.
                # if hit==false and collectPot==true, append 0. if hit==false and collectPot==false, append 1.

# DYNAMIC AI
P = np.array([])  # append [player total, dealer upcard] to array at start of hand
                # pop [] from array before start of next hand
                # X.append(P.pop())
                # RETRAIN neural net

# activation function: sigmoid
def sigmoid(x, deriv=False):
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))

'''Play game'''
while player1.chips > 0:

    '''Neural Net'''
    layer3error = np.random.random_integers(1, 1, Y.__len__())  # initialize array same size as Y, fill with 1's
    for i in layer3error:
        while abs(layer3error[i]) > .5:  # if any error is greater than .5, re-initialize & re-train
            # initialize weights
            weight1 = np.random.random((2, Y.__len__()))  # (# of arrays, # of items in each array)
            weight2 = np.random.random((Y.__len__(), 1))  # try (2*random) - 1

            # TRAIN, use for loop 1000s of times.
            number_of_training_iterations = 50000
            for iteration in range(number_of_training_iterations):
                layer1 = X  # input
                layer2 = sigmoid(np.dot(layer1, weight1))  # multiply input by weight. if > than threshold, activate.
                layer3 = sigmoid(np.dot(layer2, weight2))  # layer2 * weight2

                # backpropagate
                layer3error = Y - layer3
                layer3change = layer3error * sigmoid(layer3, deriv=True)
                layer2error = layer3change.dot(weight2.T)  # layer3change * weight2
                layer2change = layer2error * sigmoid(layer2, deriv=True)

                # update weights
                weight2 += layer2.T.dot(layer3change)  # layer2 * layer3change
                weight1 += layer1.T.dot(layer2change)  # layer1 * layer2change

                if iteration % 10000 == 0:
                    print("Error: ", layer3error[0])

    label.configure(text="" + str(player1.name) + "'s chips: " + str(player1.chips))

    # send hands to discard
    while len(player1.hand) > 0:
        discardpile.append(player1.hand.pop())
    while len(dealer1.hand) > 0:
        discardpile.append(dealer1.hand.pop())
    # delete prediction neural net data [player total, dealer upcard]
    while len(P) > 0:
        P = np.delete(P, 0)

    # if 75% of deck used, restack and reshuffle deck
    if len(discardpile) > 39:
        for c in discardpile:
            if c.getcardValue() == 1:
                c.setcardValue(11)
        while len(discardpile) > 0:
            deck1.cards.append(discardpile.pop())
        deck1.shuffle()
        print("Deck has been SHUFFLED")

    hitted = False
    win = False
    bet = False
    while not bet:
        betamount = int(simpledialog.askstring("Bet", "Bet amount?"))
        if betamount < 0:
            betamount = simpledialog.askstring("Bet", "Invalid amount. Try again")
        if betamount <= player1.chips and betamount > 0:
            player1.bet(betamount)
            bet = True
        else:
            betamount = simpledialog.askstring("Bet", "Insufficient chips. Try again")

    player1.draw()
    dealer1.draw()
    player1.draw()
    dealer1.draw()
    
    label2.configure(text="" + str(dealer1.name) + ": " + str(dealer1.hand[0].printCard()) + ": " + str(dealer1.hand[0].getcardValue()))
    label3.configure(text="" + str(player1.name) + ": " + str(player1.showHand()) + ": " + str(player1.handValue()))
    label4.configure(text="...")

    # append [player total, dealer upcard] to neural net array
    P = np.append(P, [player1.handValue(), dealer1.hand[0].getcardValue()])
    # prediction
    layer1p = P
    layer2p = sigmoid(np.dot(layer1p, weight1))
    layer3p = sigmoid(np.dot(layer2p, weight2))
    print("Given: ", P)
    print("Prediction: ", layer3p)

    # Blackjack evaluations
    if player1.blackjack():
        if dealer1.blackjack():
            dealer1.showHand()
            print("Blackjack showdown!")
            player1.collectPot(push=True)
            continue
        else:
            print("Blackjack!")
            player1.collectPot(bj=True)
            continue

    while player1.handValue() <= 21:
        acecount = 0
        while player1.handValue() < 21:
            option = messagebox.askyesno("Option", "Hit?")
            if option:
                hit()
                hitted = True
            else:
                break

        # player bust
        if player1.handValue() > 21:
            # implement ace 1/11
            if player1.handValue() == 22 and player1.hand[0].getcardValue() == 11 and player1.hand[1].getcardValue() == 11:
                player1.hand[0].setcardValue(1)
                acecount = 1
                label3.configure(
                    text="" + str(player1.name) + ": " + str(player1.showHand()) + ": " + str(player1.handValue()))
            else:
                for c in player1.hand:
                    if c.getcardValue() == 11:
                        c.setcardValue(1)
                        acecount = 1
                        label3.configure(text="" + str(player1.name) + ": " + str(player1.showHand()) + ": " + str(
                            player1.handValue()))
            if player1.handValue() > 21:
                label4.configure(text="u bust u lose")
                player1.pot = 0
                label2.configure(text="" + str(dealer1.name) + ": " + str(dealer1.showHand()) + ": " + str(dealer1.handValue()))

        if player1.handValue() < 21 and acecount > 0:  # and doublecount == 0
            continue

        elif player1.handValue() <= 21:
            # dealer hits
            while dealer1.handValue() < 17:
                dealer1.draw()
                label2.configure(
                    text="" + str(dealer1.name) + ": " + str(dealer1.showHand()) + ": " + str(dealer1.handValue()))

                # dealer bust
                if dealer1.handValue() > 21:
                    #implement ace 1/11
                    if dealer1.handValue() == 22 and dealer1.hand[0].getcardValue() == 11 \
                            and dealer1.hand[1].getcardValue() == 11:
                        dealer1.hand[0].setcardValue(1)
                        acecount = 1
                        label2.configure(
                            text="" + str(dealer1.name) + ": " + str(dealer1.hand[0].printCard()) + ": " + str(
                                dealer1.hand[0].getcardValue()))
                    else:
                        for c in dealer1.hand:
                            if c.getcardValue() == 11:
                                c.setcardValue(1)
                                label2.configure(
                                    text="" + str(dealer1.name) + ": " + str(dealer1.hand[0].printCard()) + ": " + str(
                                        dealer1.hand[0].getcardValue()))
                    if dealer1.handValue() > 21:
                        label4.configure(text="Dealer bust! u win :D")
                        player1.collectPot()
                        win = True

        # if player or dealer doesn't bust, evaluate which hand is greater
        if player1.handValue() <= 21 and dealer1.handValue() <= 21:
            label2.configure(text="" + str(dealer1.name) + ": " + str(dealer1.showHand()) + ": " + str(dealer1.handValue()))
            if player1.handValue() == dealer1.handValue():
                label4.configure(text="Push")
                player1.collectPot(push=True)
            if player1.handValue() > dealer1.handValue():
                label4.configure(text="u win :D")
                player1.collectPot()
                win = True
            if player1.handValue() < dealer1.handValue():
                label4.configure(text="gg u lose")
                player1.pot = 0

        '''Append data'''
        # if hit==true and collectPot==true, append 1. if hit==true and collectPot==false, append 0.
        # if hit==false and collectPot==true, append 0. if hit==false and collectPot==false, append 1.
        # Y
        Y = np.resize(Y, (Y.__len__() + 1, 1))
        if hitted and win:
            # Y = np.append(Y, [1])
            Y[Y.__len__() - 1] = [1]
        elif hitted and not win:
            # Y = np.append(Y, [0])
            Y[Y.__len__() - 1] = [0]
        elif not hitted and win:
            # Y = np.append(Y, [0])
            Y[Y.__len__() - 1] = [0]
        elif not hitted and not win:
            # Y = np.append(Y, [1])
            Y[Y.__len__() - 1] = [1]

        # X
        # X = np.append(X, P)  # X.append(P.pop())
        X = np.resize(X, (Y.__len__(), 2))
        X[Y.__len__() - 1] = [player1.handValue(), dealer1.hand[0].getcardValue()]

        break

window.mainloop()
