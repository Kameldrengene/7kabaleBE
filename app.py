from flask import Flask, request
from flask_restful import Resource, Api
import turnGen.SolitareChecker as SolitareChecker
from turnGen.objects.Gameboard import Gameboard

app = Flask(__name__)
api = Api(app)

def gameboardEncoder(gameboard):
    dict = {
        "deckpointer": gameboard.deckPointer,
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


class TurnGeneration(Resource):
    def post(self):
        gameboard = request.get_json()
        return {"check": SolitareChecker.checkSolitare(gameboard)}, 201

    def get(self):
        return gameboardEncoder(Gameboard())


api.add_resource(TurnGeneration, '/turn/')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
