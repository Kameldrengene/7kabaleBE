# Frederik Koefoed s195463  
# Lasse Strunge s195486
# Mark Mortensen s174881
# Mikkel Danielsen s183913
# Muhammad Talha s195475
# Volkan Isik s180103

from turnGen.objects.Gameboard import Gameboard
from turnGen.objects.Card import Card

def convertBoard(gameboard=Gameboard):
    for i in range(4):
        finspace = gameboard.finSpaceConverter[i]
        if len(gameboard.finSpaces[finspace]) != 0:
            card = gameboard.finSpaces[finspace][-1]  # Finds last card in each finSpace
            new_ls = []
            value = 1
            while value <= card.value:
                new_card = Card(card.type, value)
                new_ls.append(new_card)
                value += 1
            gameboard.finSpaces[finspace] = new_ls

    return gameboard
