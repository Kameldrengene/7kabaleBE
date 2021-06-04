from objects.Gameboard import Gameboard

typeConverter = {0: "Spar",
                 1: "Hjerter",
                 2: "Klør",
                 3: "Ruder"}

valueConverter = {1: "Es",
                  2: "2",
                  3: "3",
                  4: "4",
                  5: "5",
                  6: "6",
                  7: "7",
                  8: "8",
                  9: "9",
                  10: "10",
                  11: "Knægt",
                  12: "Dronning",
                  13: "Konge"}

def checkSolitare(gameboard):  # Should return a msg with what is wrong.
    """
    should check
    * Are there too many cards in a pile
    * are cards in 2 places at once
      * watch out for if used in finspaces
    * is the board legal?
      * cards on top of each other correctly?
        * color
        * number
      * number of hidden cards possible
        * max one with 6+ hidden
        * max two with 5+ hidden
        * ...
    """

    # Checking for too many shown cards
    for pile in gameboard.spaces:
        if len(pile.shownCards) > 13:
            return "Fejl. En bunke indeholder for mange åbne kort"

    # Checking for multiple of same card
    for i in range(len(gameboard.spaces)):
        for card in gameboard.spaces[i].shownCards:
            # in spaces pile
            count = 0
            for j in range(len(gameboard.spaces) - i):
                curr = i + j  # Current pile looking at
                for card2 in gameboard.spaces[curr].shownCards:
                    if card.value == card2.value and card.type == card2.type:
                        count += 1
                        if count > 1:  # Error found TODO
                            return "Fejl. {0} {1} findes flere stedet på brættet.".format(typeConverter[card.type], valueConverter[card.value])

            # in finspaces
            type = gameboard.finSpaceConverter[card.type]
            if len(gameboard.finSpaces[type]) != 0:
                lastCardOfType = gameboard.finSpaces[type][-1]

                if lastCardOfType.value >= card.value:
                    # Error found TODO
                    return "Fejl. {0} {1} findes både på brættet og i {0} slutpladsen.".format(typeConverter[card.type], valueConverter[card.value])

    # Checking for legal board
    for i in range(len(gameboard.spaces)):
        pile = gameboard.spaces[i]
        # correct ordering
        for j in range(len(pile.shownCards) - 1):
            k = pile.shownCards[j]  # simulates king
            q = pile.shownCards[j+1]  # simulates queen
            if k.value != q.value + 1 or not k.isDifferent(q):
                # Error found in ordering TODO
                return "Fejl. {0} {1} kan ikke ligge på {2} {3}.".format(typeConverter[q.type], valueConverter[q.value],
                                                                         typeConverter[k.type], valueConverter[k.value],)

    # Checking for legal amount of hidden cards
    for i in range(7):
        count = 0
        for pile in gameboard.spaces:
            if len(pile.hiddenCards) >= 7-i:
                count += 1
        if count > i:
            # Error in amount of hiddencards TODO
            if i == 0:
                return "Fejl. En eller flere bunker har over 6 lukkede kort."
            else:
                r = ""
                if i > 1:
                    r = "r"
                return "Fejl. For mange bunker har {0} lukkede kort. Kun {1} bunke{2} kan have {0} lukkede kort".format(
                                                                                                    str(7-i), str(i), r)

    return "OK"
