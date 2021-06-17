# Frederik Koefoed s195463  
# Lasse Strunge s195486
# Mark Mortensen s174881
# Mikkel Danielsen s183913
# Muhammad Talha s195475
# Volkan Isik s180103

from .Card import Card
from .Pile import Pile
from random import shuffle
import copy


class Gameboard:

    def __init__(self, gameboard=None):
        self.finSpaces = None
        self.deck = None
        self.deckPointer = None
        self.spaces = None
        self.finSpaceConverter = {0: "a", #spare
                                  1: "b",#hjerter
                                  2: "c",#klør
                                  3: "d"}#roder

        if gameboard is None:   # normal init with setup game
            self.setUpGame()
        elif gameboard == 0:
            self.setUpClear()
        else:   # set gameboard as gameboard given
            self.finSpaces = copy.deepcopy(gameboard.finSpaces)
            self.deck = copy.deepcopy(gameboard.deck)
            self.deckPointer = gameboard.deckPointer
            self.spaces = copy.deepcopy(gameboard.spaces)

    def setUpGame(self):
        self.finSpaces = {"a": [],
                          "b": [],
                          "c": [],
                          "d": []}
        self.deck = []
        self.deckPointer = -1
        self.spaces = []

        for i in range(4):
            for j in range(13):
                self.deck.append(Card(i, j+1))

        shuffle(self.deck)

        for i in range(7):
            hidden = [] #Backside værdi -> 14
            shown = []
            for j in range(i+1):
                if j == i:
                    shown.append(self.deck[0])
                else:
                    hidden.append(self.deck[0])

                self.deck.pop(0)

            self.spaces.append(Pile(shown, hidden))

    def setUpClear(self):
        self.finSpaces = {"a": [],
                          "b": [],
                          "c": [],
                          "d": []}
        self.deck = []
        self.deckPointer = -1
        self.spaces = []

    def draw(self):
        self.deckPointer += 1
        if self.deckPointer == len(self.deck):
            self.deckPointer = -1
        return True


    def move(self, xs, ys):
        try:
            ys = int(ys)
        except:
            raise Exception("y is not an integer")

        if not 0 <= ys <= 6:
            raise Exception("y is not 0-6")

        if xs == "q":
            if self.deckPointer == -1:
                raise Exception("No card in q")
            fromDeck = []
            fromDeck.append(self.deck[self.deckPointer])
            pile = Pile(fromDeck,[])
            if self.spaces[ys].placePile(pile):
                self.deck.pop(self.deckPointer)
                self.deckPointer -= 1
                return True

        else:
            xs = int(xs)
            if xs < 0 or 6 < xs:
                raise Exception("X is not between 0-6 or q")
            if xs == ys:
                raise Exception("x and y is the same")

            movingpile = self.spaces[xs]
            endPile = self.spaces[ys]

            pointedMoves = True
            if len(movingpile.hiddenCards) == 0 and movingpile.shownCards[0].value == 13:
                pointedMoves = False

            if movingpile.moveToPile(endPile):
                return pointedMoves

    def moveN(self, xs, ys, ns):
        try:
            ys = int(ys)
        except:
            raise Exception("y is not an integer")

        try:
            xs = int(xs)
        except:
            raise Exception("x is not an integer")

        try:
            ns = int(ns)
        except:
            raise Exception("n is not an integer")

        if ys < 0 or 6 < ys:
            raise Exception("y is not 0-6")

        if xs < 0 or xs > 6:
            raise Exception("x is not 0-6")

        if ns < 0 or 13 < ns:
            raise Exception("n is not 0-13")

        if xs == ys:
            raise Exception("x and y are the same")


        movingPile = self.spaces[xs]
        endPile = self.spaces[ys]

        if movingPile.moveToPileN(endPile, ns):
            return True


    def score(self,xs):

        if xs == "q":
            if self.deckPointer == -1:
                raise Exception("No card in q")
            card = self.deck[self.deckPointer]
            nextNeeded = len(self.finSpaces[self.finSpaceConverter[card.type]]) + 1
            if card.value == nextNeeded:
                self.finSpaces[self.finSpaceConverter[card.type]].append(card)
                self.deck.pop(self.deckPointer)
                self.deckPointer -= 1
                return True
            else:
                raise Exception("Card at pos " + xs + " can't be scored yet")


        else:
            try:
                xs = int(xs)
            except:
                raise Exception("x is not 0-6 or q")

            if xs < 0 or xs > 6:
                raise Exception("x is not 0-6 or q")

            lastIndex = len(self.spaces[xs].shownCards)-1
            card = self.spaces[xs].shownCards[lastIndex]
            nextNeeded = len(self.finSpaces[self.finSpaceConverter[card.type]]) + 1
            if card.value == nextNeeded:
                self.finSpaces[self.finSpaceConverter[card.type]].append(card)
                self.spaces[xs].shownCards.pop(lastIndex)
                if len(self.spaces[xs].shownCards) == 0 and len(self.spaces[xs].hiddenCards) != 0:
                    hiddenLastIndex = len(self.spaces[xs].hiddenCards) - 1
                    self.spaces[xs].shownCards.append(self.spaces[xs].hiddenCards.pop(hiddenLastIndex))
                return True
            else:
                raise Exception("Card at pos " + str(xs) + " can't be scored yet")


    def remove(self,ks,ys):
        if len(ks) != 1 or len(ys) != 1:
            raise Exception("Error in input")

        if ks != "a" and ks != "b" and ks != "c" and ks != "d":
            raise Exception("k is not a-d")

        try:
            ys = int(ys)
        except:
            raise Exception("y is not 0-6")

        if ys < 0 or 6 < ys:
            raise Exception("y is not 0-6")

        lastFinIndex = len(self.finSpaces[ks]) - 1
        if lastFinIndex == -1:
            raise Exception("No cards in pos " + ks)
        finCard = self.finSpaces[ks][lastFinIndex]

        lastSpaceIndex = len(self.spaces[ys].shownCards) - 1

        if finCard.value == 13 and lastSpaceIndex == -1:
            self.spaces[ys].shownCards.append(finCard)
            self.finSpaces[ks].pop(lastFinIndex)
            return True

        if lastSpaceIndex == -1:
            raise Exception("Can't return card from pos " + ks + " to pos " + str(ys))

        spaceCard = self.spaces[ys].shownCards[lastSpaceIndex]

        if finCard.isDifferent(spaceCard) and finCard.value + 1 == spaceCard.value:
            self.spaces[ys].shownCards.append(finCard)
            self.finSpaces[ks].pop(lastFinIndex)
            return True
        else:
            raise Exception("Can't return card from pos " + ks + " to pos " + str(ys))


    def isWon(self):
        win = True
        for key in range(7):
            if len(self.spaces[key].hiddenCards) != 0:
                win = False
                break
        return win
