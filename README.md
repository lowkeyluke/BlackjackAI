# BlackjackAI
Basic, 4-layer FCN implemented 'from scratch' (no dedicated NN library; only numpy) in order to demonstrate understanding of basic, fundamental concepts on NNs.
Toy problem: Blackjack

- 'Online Training'; re-trains on new observations/data during 'live play'

#
Files needed: 
- blackjack.py : contains all classes/objects (deck, card, player, dealer, etc.) & their respective methods
- layer4.py : 'driver' file that runs the game & provides a GUI
(All other files are more or less test files)

Summary of command-line output:
- training info
- NN's output of whether to 'hit' or 'stand' [0-1]
  - the value can be thought of as the NN's 'confidence' to hit, with 0.5 being the decision boundary between standing or hitting 
(e.g. 0 = 100% confidence in standing, 0% confidence to hit. 0.5 = idfk?! 1 = 0% confidence to stand, 100% confidence in hitting)
