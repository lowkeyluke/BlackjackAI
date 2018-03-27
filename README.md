# BlackjackAI
Neural network that predicts how to win blackjack by:

-Gathering data while you play

-Retraining itself using this data in order to strengthen its predictions.

Files needed: blackjack.py, layer4.py
(All other files are more or less test files.)

blackjack.py contains all classes/objects (deck, card, player, dealer, etc.), 
and their respective methods.

layer4.py is the driver file that runs the GUI and the game. 
Printed on the command-line:
-The neural net's training.
-The neural net's prediction to hit or stand [0-1].
The value is a measurement of the neural net's confidence to hit (draw a card).
0 = 100% confidence to stand. 0% confidence to hit.
.5 = 50% confidence to stand. 50% confidence to hit.
1 = 0% confidence to stand. 100% confidence to hit.
