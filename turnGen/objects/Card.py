# Frederik Koefoed s195463  
# Lasse Strunge s195486
# Mark Mortensen s174881
# Mikkel Danielsen s183913
# Muhammad Talha s195475
# Volkan Isik s180103

class Card:
    def __init__(self, type, value):
        self.type = type #0: spar 1: Hjerter 2: Klør 3: Ruder
        self.value = value

    def isRed(self):
        return 1 == self.type % 2

    def isBlack(self):
        return 0 == self.type % 2

    def isDifferent(self, newCard):
        return newCard.type % 2 != self.type % 2
