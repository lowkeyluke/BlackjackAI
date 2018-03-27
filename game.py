"""Play fully inclusive blackjack on the command-line
with all special functions: double, split, versatile ace, etc.
No neural net."""

from blackjack import *

#set up game
deck1.shuffle()
discardpile = []
printScores()
name = input("Welcome to lowkeyluke's BlackJack! What's your name?")
player1 = Player(name)
dealer1 = Dealer("THE DEALER")
if name == "Luke":
    print("Welcome back Master!")
else:
    print("bet 0 to exit, bet -1 to save, bet then type save to retrieve save (type all inputs as lowercase)")
    print("Good luck,", name+"!")

#play game
while player1.chips > 0:
    print(player1.name + "'s chips:", player1.chips)

    # send hands to discard
    while len(player1.hand) > 0:
        discardpile.append(player1.hand.pop())
    while len(dealer1.hand) > 0:
        discardpile.append(dealer1.hand.pop())

    # if 75% of deck used, restack and reshuffle deck
    if len(discardpile) > 39:
        for c in discardpile:
            if c.getcardValue() == 1:
                c.setcardValue(11)
        while len(discardpile) > 0:
            deck1.cards.append(discardpile.pop())
        deck1.shuffle()
        print("Deck has been SHUFFLED")

    bet = False
    betamount = int(input("Enter bet amount:"))
    while not bet:
        if betamount == 0:
            exitoption(69)
            exit(69)
        if betamount == -1:
            exitoption(70)
            exitoption(69)
            exit(70)
        if betamount < 0:
            betamount = int(input("Invalid amount. Try again"))
        if betamount <= player1.chips and betamount > 0:
            player1.bet(betamount)
            bet = True
        else: betamount = int(input("Insufficient chips. Try again"))

    dealerbj = False
    player1.draw()
    dealer1.draw()
    player1.draw()
    dealer1.draw()
    print(dealer1.name + ":")
    dealer1.hand[0].printCard()
    # dealer1.showHand()
    player1.showHand()

    #BlackJack evaluations
    if dealer1.hand[0].getcardValue() == 11: #if first dealer card is an Ace
        insurance = input("Insurance?")
        if insurance == "yes":
            player1.insurance(betamount)
            if dealer1.blackjack():
                dealer1.showHand()
                print("Dealer Blackjack insured")
                player1.chips += betamount * 1.5
                player1.pot = 0
                continue
            elif not dealer1.blackjack(): print("You lost your insurance")
        elif dealer1.blackjack():
            dealer1.showHand()
            print("Dealer Blackjack")
            player1.pot = 0
            continue

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

    splitcount = 0
    doublecount = 0
    while player1.handValue() <= 21 or \
            (player1.handValue() == 22 and player1.hand[0].getcardValue() == 11 and player1.hand[1].getcardValue() == 11):
        acecount = 0
        while player1.handValue() < 21:
            if player1.hand[0].getcardValue() == player1.hand[1].getcardValue() and splitcount == 0:
                option = input("Split/Double/Hit/Stand?")
            elif len(player1.hand) == 2:
                option = input("Double/Hit/Stand?")
            elif len(player1.hand) > 2:
                option = input("Hit/Stand?")
            if option == "exit":
                exitoption(69)
                exit(69)
            if option == "save":
                player1.pot = 0
                nametxt = name + ".txt"
                SCFile = open(nametxt, "r")
                chips = int(SCFile.read())
                player1.chips = chips
                break
            if option == "hit":
                player1.draw()
                player1.showHand()
            if option == "stand":
                break
            if option == "double":
                doublecount = 1
                player1.bet(betamount)
                player1.draw()
                player1.showHand()
                break
            if option == "split" and splitcount == 0:
                splitcount=1
                player1.splithand.append(player1.hand.pop())
                player1.draw()
                player1.showHand()
        if option == "save":
            break
        # SPLIT
        if len(player1.splithand) > 0:
            splitcount = 1
            #if player busts on first hand, player must play second hand before dealer draws.
            if player1.handValue() > 21:
                #implement ace 1/11
                for c in player1.hand:
                    if c.getcardValue() == 11:
                        c.setcardValue(1)
                        acecount=1
                if player1.handValue() > 21:
                    print("u bust u lose")
                    player1.pot = 0
            if player1.handValue() < 21 and acecount > 0 and doublecount == 0:
                continue
            # save first hand value
            temphandvalue = player1.handValue()
            # player 1 makes same bet for second hand
            player1.bet(betamount)
            player1.draw(split=True)
            # send first hand to discard pile
            while len(player1.hand) > 0:
                discardpile.append(player1.hand.pop())
            while len(player1.splithand) > 0:
                player1.hand.append(player1.splithand.pop())
            player1.showHand()
            continue

        #player bust

        if player1.handValue() > 21:
            # implement ace 1/11
            if player1.handValue() == 22 and player1.hand[0].getcardValue() == 11 and player1.hand[1].getcardValue() == 11:
                player1.hand[0].setcardValue(1)
                acecount = 1
            else:
                for c in player1.hand:
                    if c.getcardValue() == 11:
                        c.setcardValue(1)
                        acecount = 1
            if player1.handValue() > 21:
                print("u bust u lose")
                player1.pot = 0
                dealer1.showHand()

        if player1.handValue() < 21 and acecount > 0 and doublecount == 0:
            continue

        elif player1.handValue() <= 21:
            #dealer hits
            while dealer1.handValue() < 17:
                dealer1.draw()
                dealer1.showHand()

                #dealer bust
                if dealer1.handValue() > 21:
                    if dealer1.handValue() == 22 and dealer1.hand[0].getcardValue() == 11 \
                            and dealer1.hand[1].getcardValue() == 11:
                        dealer1.hand[0].setcardValue(1)
                        acecount = 1
                    else:
                        for c in dealer1.hand:
                            if c.getcardValue() == 11:
                                c.setcardValue(1)
                    if dealer1.handValue() > 21:
                        print("Dealer bust! u win :D")
                        player1.collectPot()

        #if player or dealer doesn't bust, evaluate which hand is greater
        if splitcount > 0:
            dealer1.showHand()
            if temphandvalue <=21 and dealer1.handValue() <= 21:
                print(temphandvalue, "vs.", dealer1.handValue())
                if temphandvalue == dealer1.handValue():
                    print("Push split")
                    player1.collectPot(push=True, split=True)
                if temphandvalue > dealer1.handValue():
                    print("u win :D split")
                    player1.collectPot(split=True)
                if temphandvalue < dealer1.handValue():
                    print("gg u lose split")
                    player1.pot = player1.pot/2
        if player1.handValue() <= 21 and dealer1.handValue() <= 21:
            dealer1.showHand()
            print(player1.handValue(), "vs.", dealer1.handValue())
            if player1.handValue() == dealer1.handValue():
                print("Push")
                player1.collectPot(push=True)
            if player1.handValue() > dealer1.handValue():
                print("u win :D")
                player1.collectPot()
            if player1.handValue() < dealer1.handValue():
                print("gg u lose")
                player1.pot = 0
        break
exitoption(69)