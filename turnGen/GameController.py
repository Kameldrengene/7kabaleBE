from turnGen.objects.Gameboard import Gameboard


class GameController:

    def __init__(self, gameBoard=None):
        self.gameboard = Gameboard(gameBoard)
        self.score = 0
        self.turns = 0
        self.switcher = {
            "move"  : self.move,
            "m"     : self.move,
            "draw"  : self.draw,
            "d"     : self.draw,
            "score" : self.scoreFunc,
            "s"     : self.scoreFunc,
            "return": self.remove,
            "r"     : self.remove
        }

    def move(self, exe):
        if len(exe) == 3:
            x = exe[1]
            y = exe[2]
            if self.gameboard.move(x, y):  # will be false if a king from a king move is tried to be moved
                self.score += 5
            self.turns += 1
            return True
        elif len(exe) == 4:
            x = exe[1]
            y = int(exe[2])
            n = int(exe[3])
            if self.gameboard.moveN(x, y, n):  # Will be true if a new card is revealed
                self.score += 5
            self.turns += 1
            return True
        return False

    def draw(self, exe):
        if self.gameboard.draw():
            self.turns += 1
            self.score += 1
            return True
        return False

    def scoreFunc(self, exe):
        if len(exe) == 2:
            if self.gameboard.score(exe[1]):
                self.score += 10
            self.turns += 1
            return True
        return False        # shouldn't happen

    def remove(self, exe):
        if len(exe) == 3:
            if self.gameboard.remove(exe[1], exe[2]):
                self.score -= 10

            self.turns += 1
            return True
        return False

    def unknown(self, exe):
        raise Exception("Command not found")

    def executeCommand(self, command=str):
        exe = command.split(" ")
        if self.switcher.get(exe[0], self.unknown)(exe):
            if self.gameboard.isWon():
                self.score = 655
            return True
        raise Exception("Error in command input")




