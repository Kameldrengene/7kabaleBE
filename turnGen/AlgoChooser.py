from objects.Gameboard import Gameboard
from objects.Card import Card
from objects.Pile import Pile


def eval_board(gameboard):
    best = []

    for pair in getMovables(gameboard):  # find all moves possible
        if len(best) == 0:
            best = pair
        else:  # Choose best movable from most hidden cards
            if len(gameboard.spaces[best[0]].hiddenCards) < len(gameboard.spaces[pair[0]].hiddenCards):  # finds the move with most possible cards in hiddenCards
                best = pair

    if len(best) != 0:
        return ["m {0} {1}".format(best[0], best[1])]

    for i in range(7):  # check if any card on board is scorable
        if len(gameboard.spaces[i].shownCards) != 0:
            if isScorable(gameboard.spaces[i].shownCards[-1], gameboard):
                return ["s {0}".format(i)]


    movable = movablesByReturning(gameboard) #is it possible to return something from the scoring fields to move something around on the board?
    if movable != -1:
        return movable

    #is it possible to move n in order to score a card?
    for pile in range(len(gameboard.spaces)): #loops through all piles
        for card in range(len(gameboard.spaces[pile].shownCards)): #loops through every card in each pile
            for k in range(4): # loops through the finish spaces
                finspace = gameboard.finSpaceConverter[k]
                space = gameboard.finSpaces[finspace]

                if gameboard.spaces[pile].shownCards[card].value == len(space) + 1 and gameboard.spaces[pile].shownCards[card].type == k: #if card is scorable on current finish space
                    if card + 1 > len(gameboard.spaces[pile].shownCards) or len(gameboard.spaces[pile].shownCards) == 0: #stops if the lowest card in the pile or no cards in pile
                        break
                    else:
                        moveCard = card + 1

                    for pile2 in range(len(gameboard.spaces)):
                        if len(gameboard.spaces[pile2].shownCards) == 0: #stops if pile2 has no cards in it
                            break
                        if gameboard.spaces[pile2].shownCards[-1].value == gameboard.spaces[pile].shownCards[moveCard].value + 1 and gameboard.spaces[pile2].shownCards[-1].type % 2 != gameboard.spaces[pile].shownCards[moveCard].type % 2: #is the value moveable
                            n = len(gameboard.spaces[pile].shownCards)-moveCard
                            return ["m {0} {1} {2}".format(pile, pile2, n)]


    if gameboard.deckPointer != -1:  # see if card in deck is usable
        deckCard = gameboard.deck[gameboard.deckPointer]

        for i in range(7):  # if card in deck is movable to board, then do that
            if len(gameboard.spaces[i].shownCards) == 0:
                if deckCard.value == 13:
                    return ["m q {0}".format(i)]
            elif deckCard.isDifferent(gameboard.spaces[i].shownCards[-1]) and deckCard.value == gameboard.spaces[i].shownCards[-1].value-1:
                return ["m q {0}".format(i)]

        if isScorable(deckCard, gameboard):  # is card in deck scorable, then score
            return ["s q"]



    return ["d"]


def isScorable(card, gameboard):  # compares card to correct finspace to see if scorable
    type = card.type
    finSpaceConverter = {0: "a",
                         1: "b",
                         2: "c",
                         3: "d"}
    finSpacePointer = finSpaceConverter[type]
    if len(gameboard.finSpaces[finSpacePointer]) != 0:
        currCard = gameboard.finSpaces[finSpacePointer][-1]
    else:
        currCard = Card(type, 0)

    if currCard.value == card.value-1:
        return True
    return False


def getMovables(gameboard):  # getting list of movable moves in format [[x1,y1],[x2,y2],...]
    movables = []
    for i in range(7):
        for j in range(7):
            if i != j:
                if len(gameboard.spaces[i].shownCards) == 0:  # if no cards to be moved
                    continue

                endCard = gameboard.spaces[i].shownCards[0]
                if endCard.value == 1:  # if trying to move an Ace
                    continue

                if len(gameboard.spaces[j].shownCards) == 0:  # if moving to empty space
                    if len(gameboard.spaces[i].hiddenCards) == 0:  # case where moving from kingspace to kingspace
                        continue
                    if endCard.value == 13:  # case where king trying to move to kingspace
                        movables.append([i, j])
                    continue
                else:
                    startCard = gameboard.spaces[j].shownCards[-1]
                    if startCard.isDifferent(endCard) and startCard.value == endCard.value+1:  # if correct colors and 1 value from each other
                        movables.append([i, j])

    return movables

def movablesByReturning(gameboard):
    for i in range(7):
        for j in range(7):
            if i != j:
                if len(gameboard.spaces[i].shownCards) == 0:
                    continue

                endCard = gameboard.spaces[i].shownCards[0]
                if endCard.value == 1:
                    continue

                if len(gameboard.spaces[j].shownCards) == 0:
                    continue

                else:
                    startCard = gameboard.spaces[j].shownCards[-1]
                    if not startCard.isDifferent(endCard) and endCard.value == startCard.value-2:
                        for k in range(4):
                            finspace = gameboard.finSpaceConverter[k]
                            space = gameboard.finSpaces[finspace]

                            if startCard.type % 2 != k % 2: #if the card is not the same type as the finishSpace
                                if len(space) == endCard.value+1: #does the card have the value between startCard and endCard


                                    return ["r {0} {1}".format(finspace, j), "m {0} {1}".format(i, j)]
    return -1

