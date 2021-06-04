from turnGen.objects.Gameboard import Gameboard
from turnGen.objects.Card import Card

def convertBoard(gameboard=Gameboard):
    for i in range(4):
        finspace = gameboard.finSpaceConverter[i]
        card = gameboard.finSpaces[finspace][-1]  # Finds last card in each finSpace
        new_ls = []
        value = 1
        while value <= card.value:
            new_card = Card(card.type, value)
            new_ls.append(new_card)
        gameboard.finSpaces[finspace] = new_ls

    return gameboard