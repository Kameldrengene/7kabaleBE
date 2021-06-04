import copy
from turnGen.objects.Card import Card

class Pile:

    def __init__(self, shownCards, hiddenCards):
        self.shownCards = shownCards
        self.hiddenCards = hiddenCards

    def placePile(self, pile):

        #if empty
        if len(self.shownCards) == 0 and len(self.hiddenCards) == 0:

            if pile.shownCards[0].value == 13:
                self.shownCards.extend(pile.shownCards.copy())
                return True
            raise Exception("Only kings may be moved to a free spot")


        # if cards are already here
        if len(self.shownCards) != 0:
            firstCard = self.shownCards[len(self.shownCards)-1] #First card already in pile
            newCard = pile.shownCards[0] #new card being put on first card

            if firstCard.isDifferent(newCard) and firstCard.value == newCard.value + 1:
                self.shownCards.extend(pile.shownCards)
                return True

            raise Exception("The cards can't be placed in that position")
        raise Exception("Error in placePile")



    def moveToPile(self, pile):

        if len(self.shownCards) == 0: #No cards
            raise Exception("No cards in pile")

        if pile.placePile(self):
            self.shownCards = [] #remove all shown cards

            if len(self.hiddenCards) != 0: #if there is a hidden card left
                lastHiddenPos = len(self.hiddenCards)-1
                self.shownCards.append(self.hiddenCards[lastHiddenPos]) #make the hidden card a shown card
                self.hiddenCards.pop(lastHiddenPos) #remove the card from the hidden card list

            return True


    def moveToPileN(self,pile, n): #moves n cards from a pile
        if len(self.shownCards) < n: #if you try to move more cards than in the pile
            raise Exception("Not enough cards in pile")

        subShownList = []
        for i in range(n):
            lastIndex = len(self.shownCards)-1
            subShownList.insert(0, self.shownCards[lastIndex])
            self.shownCards.pop(lastIndex)

        subCopy = []
        for card in subShownList:
            subCopy.append(Card(card.type, card.value))

        subPile = Pile(subShownList,[])

        try:
            if pile.placePile(subPile):
                if len(self.hiddenCards) != 0 and len(self.shownCards) == 0:
                    self.shownCards.append(self.hiddenCards.pop(-1))
                    return True

                return False
            raise Exception("Can't move that subpile there.")

        except Exception as e:
            self.shownCards.extend(subCopy)
            raise e




