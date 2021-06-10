from turnGen.objects.Gameboard import Gameboard
import random
from time import time

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


def convertInstructions(commands=[], gameboard=Gameboard):
    msg_list = []
    for command in commands:
        command = command.split(" ")

        if command[0] == "m":  # move
            x = command[1]
            y = int(command[2])
            if len(command) == 3:

                isPile = False
                if x == "q":
                    card_to_move = gameboard.deck[gameboard.deckPointer]
                else:
                    x = int(x)
                    card_to_move = gameboard.spaces[x].shownCards[0]
                    if len(gameboard.spaces[x].shownCards) > 1:
                        isPile = True

                if len(gameboard.spaces[y].shownCards) == 0:
                    card_to_end = None
                else:
                    card_to_end = gameboard.spaces[y].shownCards[-1]

                msg = "Ryk "
                if isPile:
                    msg += "bunken med "
                if not card_to_end is None:
                    msg += "{0} {1} oven på {2} {3}.".format(typeConverter[card_to_move.type], valueConverter[card_to_move.value],
                                                     typeConverter[card_to_end.type], valueConverter[card_to_end.value])
                else:
                    msg += "{0} {1} til en kongeplads.".format(typeConverter[card_to_move.type], valueConverter[card_to_move.value])
                msg_list.append(msg)

            elif len(command) == 4:
                n = int(command[3])
                isPile = False
                x = int(x)
                card_to_move = gameboard.spaces[x].shownCards[n * (-1)]
                if n > 1:
                    isPile = True

                card_to_end = gameboard.spaces[y].shownCards[-1]

                msg = "Ryk "
                if isPile:
                    msg += "bunken med "
                msg += "{0} {1} oven på {2} {3}.".format(typeConverter[card_to_move.type],
                                                         valueConverter[card_to_move.value],
                                                         typeConverter[card_to_end.type],
                                                         valueConverter[card_to_end.value])
                msg_list.append(msg)


        elif command[0] == "s":  # score
            x = command[1]

            if x == "q":
                card_to_score = gameboard.deck[gameboard.deckPointer]
            else:
                x = int(x)
                card_to_score = gameboard.spaces[x].shownCards[-1]
            msg = "Ryk {0} {1} til {0} målfeltet.".format(typeConverter[card_to_score.type], valueConverter[card_to_score.value])
            msg_list.append(msg)

        elif command[0] == "r":  # return
            k = command[1]
            y = int(command[2])

            card_to_move = gameboard.finSpaces[k][-1]
            card_to_end = gameboard.spaces[y].shownCards[-1]  # will never move to kingspace

            msg = "Ryk {0} {1} fra {0} målfeltet oven på {2} {3}.".format(
                typeConverter[card_to_move.type], valueConverter[card_to_move.value],
                typeConverter[card_to_end.type], valueConverter[card_to_end.value])
            msg_list.append(msg)

        elif command[0] == "d":  # draw
            msg = "Træk et nyt kort fra bunken."
            msg_list.append(msg)

        elif command[0] == "n":  # nothing to do
            msg = "Ingen træk kan tages. Spillet er slut."
            msg_list.append(msg)

        else:
            raise Exception("Command not convertible: {0}".format(command[0]))

    msg = ""
    if gameboard.isWon():
        random.seed(round(time()*1000))
        if random.randint(1, 100) == 100:
            msg += "Du er lidt en spade hvis du ikke kan løse kabalen herfra -Lasse 2021\n"
        else:
            msg += "Alle kort er tilgængelige og spillet er vundet\n"

    if len(msg_list) == 1:
        msg += msg_list[0]
    else:
        for i in range(len(msg_list)):
            msg += "{0}. {1}\n".format(i+1, msg_list[i])

    return msg