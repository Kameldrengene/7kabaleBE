from flask import Flask, request
from flask_restful import Resource, Api
import turnGen.SolitareChecker as SolitareChecker
from turnGen.objects.Card import Card
from turnGen.objects.Pile import Pile
from turnGen.objects.Gameboard import Gameboard
import json

app = Flask(__name__)
api = Api(app)

def gameboardEncoder(gameboard):
    dict = {
        "deckPointer": gameboard.deckPointer,
        "finSpaceConverter": gameboard.finSpaceConverter,
        "deck": [],
        "spaces": [],
        "finSpaces": {"a": [],
                      "b": [],
                      "c": [],
                      "d": []}
    }

    for card in gameboard.deck:
        dict["deck"].append({"type": card.type, "value": card.value})

    for pile in gameboard.spaces:
        pileDict = {
            "shownCards": [],
            "hiddenCards": []
        }
        for card in pile.shownCards:
            pileDict["shownCards"].append({"type": card.type, "value": card.value})

        for card in pile.hiddenCards:
            pileDict["hiddenCards"].append({"type": card.type, "value": card.value})

        dict["spaces"].append(pileDict)

    for type in "a","b","c","d":
        dict["finSpaces"][type] = []
        for card in gameboard.finSpaces[type]:
            dict["finSpaces"][type].append({"type": card.type, "value": card.value})

    return dict

def gameboardDecoder(json):
    gameboard = Gameboard(0)  # setup a clean gameboard

    # setting deckpointer
    gameboard.deckPointer = json["deckPointer"]

    # setting deck
    for card in json["deck"]:
        gameboard.deck.append(Card(card["type"], card["value"]))

    # setting spaces with Piles
    for pile in json["spaces"]:

        shownCards = []
        hiddenCards = []

        for card in pile["shownCards"]:
            shownCards.append(Card(card["type"], card["value"]))

        for card in pile["hiddenCards"]:
            hiddenCards.append(Card(card["type"], card["value"]))

        gameboard.spaces.append(Pile(shownCards, hiddenCards))

    # setting finSpaces
    for type in "a","b","c","d":
        for card in json["finSpaces"][type]:
            gameboard.finSpaces[type].append(Card(card["type"], card["value"]))

    return gameboard


class TurnGeneration(Resource):
    def post(self):
        gameboard = gameboardDecoder(request.get_json())
        return {"check": SolitareChecker.checkSolitare(gameboard)}, 201

    def get(self):
        return gameboardEncoder(Gameboard())


api.add_resource(TurnGeneration, '/turn/')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
