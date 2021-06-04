from BoardConverter import *
from View import View
from turnGen.objects.Gameboard import Gameboard
from GameController import GameController
import AlgoChooser
import SolitareChecker
import InstructionConverter
import os

# max score is 655

print("starter...")

W = 0
L = 0

gameboard = Gameboard()
# testing 2 of same in board
while len(gameboard.spaces[0].shownCards) < 14:
    gameboard.spaces[0].shownCards.append(Card(0,13))
print(SolitareChecker.checkSolitare(gameboard))
# passed


gameboard = Gameboard()
# testing 2 of same in board
cardToCopy = gameboard.spaces[6].shownCards[0]
gameboard.spaces[0].shownCards[0] = Card(cardToCopy.type, cardToCopy.value)
print(SolitareChecker.checkSolitare(gameboard))
# passed


gameboard = Gameboard()
# testing 2 of same in board and finspaces
cardToCopy = gameboard.spaces[0].shownCards[0]
type = gameboard.finSpaceConverter[cardToCopy.type]
gameboard.finSpaces[type].append(cardToCopy)
print(SolitareChecker.checkSolitare(gameboard))
# passed


gameboard = Gameboard()
# testing incorrect order
gameboard.spaces[0].shownCards.append(Card(0,13))
print(SolitareChecker.checkSolitare(gameboard))
# passed

gameboard = Gameboard()
# testing wrong amount of hidden
gameboard.spaces[0].hiddenCards.append(Card(0,13))
gameboard.spaces[0].hiddenCards.append(Card(0,13))
gameboard.spaces[0].hiddenCards.append(Card(0,13))
print(SolitareChecker.checkSolitare(gameboard))
# passed



"""
for i in range(1000):  # round 1: 37.082/100.000 wins  round 2: 37.076/100.000 wins round 3: 36.493/100.000 wins
    if i % 100 == 0:
        print("Running {0}".format(i))
    draws = 0
    game = GameController()
    while draws < 30 and not game.gameboard.isWon():
        commands = AlgoChooser.eval_board(game.gameboard)
        if commands[0] == "d":
            draws += 1
        else:
            draws = 0
        for command in commands:
            game.executeCommand(command)
    if game.gameboard.isWon():
        W += 1
    else:
        L += 1


print("Winrate: {0} %".format((W/(W+L))*100))

view = View()

view.startGame()
"""
