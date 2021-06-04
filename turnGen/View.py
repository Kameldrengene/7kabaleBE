from GameController import GameController
from turnGen.objects.Card import Card as Card2
import AlgoChooser
import InstructionConverter


class View:

    def __init__(self):
        self.game = GameController()

        self.top = "┌{0}┐"
        self.line = "──"
        self.topContinue = "├{0}┤"
        self.mid = "│{0}│"
        self.side = "│"
        self.end = "└{0}┘"
        self.empty = "      "

        self.valueMap = {1: "A",
                         2: "2",
                         3: "3",
                         4: "4",
                         5: "5",
                         6: "6",
                         7: "7",
                         8: "8",
                         9: "9",
                         10: "10",
                         11: "J",
                         12: "Q",
                         13: "K"}

        self.typeMap = {0: "♠",
                        1: "♥",
                        2: "♣",
                        3: "♦"}


    def helpplease(self):
        print("Commands")
        print("'help'         displays this msg")
        print("'move/m x y'   moves all cards from pos x to pos y (x [q,0-6], y [0-6])")
        print("'move/m x y n' moves the n first cards from pos x to pos y (x [0-6], y [0-6], n [1-13])")
        print("'score/s x'    moves the first card from pos x to correct end spot (x [q,0-6])")
        print("'return/r k y' moves the first card from pile k to pos x (k [a-d], y [0-6])")
        print("'draw' / 'd'   draws 1 card to pos q/resets deck if no cards available")

    def startGame(self):
        msg = ""
        self.helpplease()
        while True:
            self.printCurrent()
            if self.game.gameboard.isWon():
                msg += " -- SPILLET ER VUNDET! --"

            print("message: " + msg)
            msg = ""

            print("Score: {0}".format(self.game.score) + "   turns: {0}".format(self.game.turns))

            print("Write instruction!")
            try:
                command = input()
                if command == "help" or command == "commands":
                    self.helpplease()
                else:
                    commands = AlgoChooser.eval_board(self.game.gameboard)
                    print(InstructionConverter.convertInstructions(commands, self.game.gameboard), end=" ")
                    for command in commands:
                        print(command)
                        self.game.executeCommand(command)
            except Exception as e:
                msg = str(e)


    def printCurrent(self):
        self.printTop()
        self.printBottom()

    def printTop(self):
        finSpaces = self.game.gameboard.finSpaces
        deck = self.game.gameboard.deck
        deckPointer = self.game.gameboard.deckPointer

        startLine = """_________________________________________________
  a♠     b♥     c♣     d♦   """ + self.empty + "   q     deck\n"
        spaceLine = "│    │ │    │ │    │ │    │ " + self.empty + " │    │ │    │ \n"

        out = startLine
        s = ""

        if len(finSpaces["a"]) != 0:
            spade = finSpaces["a"][-1]
        else:
            spade = Card2(0, -1)

        if len(finSpaces["b"]) != 0:
            heart = finSpaces["b"][-1]
        else:
            heart = Card2(1, -1)

        if len(finSpaces["c"]) != 0:
            clover = finSpaces["c"][-1]
        else:
            clover = Card2(2, -1)

        if len(finSpaces["d"]) != 0:
            ruby = finSpaces["d"][-1]
        else:
            ruby = Card2(3, -1)

        shownFinCards = []
        shownFinCards.append(spade)
        shownFinCards.append(heart)
        shownFinCards.append(clover)
        shownFinCards.append(ruby)

        # First line

        for card in shownFinCards:
            if card.value == -1:
                s = self.line + self.line
            elif card.value == 10:
                s = self.typeMap[card.type] + "10" + self.typeMap[card.type]
            else:
                s = self.valueMap[card.value] + self.typeMap[card.type] + self.line
            out += (self.top.format(s)) + " "

        out += self.empty + " "

        if deckPointer == -1:
            s = self.line + self.line
        else:
            card = deck[deckPointer]
            if card.value == 10:
                s = self.typeMap[card.type] + "10" + self.typeMap[card.type]
            else:
                s = self.valueMap[card.value] + self.typeMap[card.type] + self.line

        out += (self.top.format(s)) + " "

        s = self.line + self.line
        out += (self.top.format(s)) + " \n"

        # second line
        out += spaceLine

        # third line
        for card in shownFinCards:
            if card.value == -1:
                s = "    "
            elif card.value == 10:
                s = self.typeMap[card.type] + "10" + self.typeMap[card.type]
            else:
                s = " " + self.valueMap[card.value] + self.typeMap[card.type] + " "
            out += (self.mid.format(s)) + " "

        out += self.empty + " "

        if deckPointer == -1:
            s = "    "
        else:
            card = deck[deckPointer]
            if card.value == 10:
                s = self.typeMap[card.type] + "10" + self.typeMap[card.type]
            else:
                s = " " + self.valueMap[card.value] + self.typeMap[card.type] + " "

        out += (self.mid.format(s)) + " "

        cardsInDeck = str(len(deck) - (deckPointer + 1))
        if len(cardsInDeck) == 2:
            s = " " + cardsInDeck + " "
        else:
            s = "  " + cardsInDeck + " "

        out += (self.mid.format(s)) + " \n"

        # fourth line
        out += spaceLine

        # Last line

        for card in shownFinCards:
            if card.value == -1:
                s = self.line + self.line
            elif card.value == 10:
                s = self.typeMap[card.type] + "10" + self.typeMap[card.type]
            else:
                s = self.line + self.valueMap[card.value] + self.typeMap[card.type]
            out += (self.end.format(s)) + " "

        out += self.empty + " "

        if deckPointer == -1:
            s = self.line + self.line
        else:
            card = deck[deckPointer]
            if card.value == 10:
                s = self.typeMap[card.type] + "10" + self.typeMap[card.type]
            else:
                s = self.line + self.valueMap[card.value] + self.typeMap[card.type]

        out += (self.end.format(s)) + " "

        s = self.line + self.line
        out += (self.end.format(s)) + " \n"

        print(out)

    def printBottom(self):

        startLine = "   0      1      2      3      4      5      6  \n"

        collected = []
        for i in range(7):
            prints = []
            curr = self.game.gameboard.spaces[i]

            for card in curr.hiddenCards:
                if len(prints) == 0:
                    used = self.top
                else:
                    used = self.topContinue
                prints.append(used.format(self.line+self.line))

            lastCard = None
            for card in curr.shownCards:
                lastCard = card
                if len(prints) == 0:
                    used = self.top
                else:
                    used = self.topContinue
                if card.value == 10:
                    prints.append(used.format(self.typeMap[card.type] + self.valueMap[card.value] + self.typeMap[card.type]))
                else:
                    prints.append(used.format(self.valueMap[card.value] + self.typeMap[card.type] + self.line))

            prints.append(self.mid.format("    "))
            if lastCard is None:
                for j in range(5):
                    prints.append(self.empty)
            else:

                if lastCard.value == 10:
                    prints.append(self.mid.format(self.typeMap[lastCard.type] + self.valueMap[lastCard.value] + self.typeMap[lastCard.type]))
                else:
                    prints.append(self.mid.format(" " + self.valueMap[lastCard.value] + self.typeMap[lastCard.type] + " "))

                prints.append(self.mid.format("    "))

                if lastCard.value == 10:
                    prints.append(self.end.format(self.typeMap[lastCard.type] + self.valueMap[lastCard.value] + self.typeMap[lastCard.type]))
                else:
                    prints.append(self.end.format(self.line + self.valueMap[lastCard.value] + self.typeMap[lastCard.type]))

            collected.append(prints)

        x = 0
        for a in collected:
            if len(a) > x:
                x = len(a)

        out = startLine
        i = 0
        while i < x:
            for a in collected:
                if i < len(a):
                    out += a[i]
                else:
                    out += self.empty
                out += " "

            out += "\n"

            i += 1

        print(out)


