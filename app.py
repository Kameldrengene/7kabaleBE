# !flask/bin/python
from flask import *
from flask_restful import Resource, Api
from datetime import datetime
from turnGen.objects.Gameboard import Gameboard
from turnGen.objects.Gameboard import Card
from turnGen.objects.Gameboard import Pile
import turnGen.SolitareChecker as SolitareChecker
import turnGen.InstructionConverter as InstructionConverter
import turnGen.AlgoChooser as AlgoChooser


app = Flask(__name__)
api = Api(app)

def gameboardEncoder(gameboard):
    dict = {
        "deckPointer": gameboard.deckPointer,
        "finSpaceConverter": gameboard.finSpaceConverter,
        "deck": [],
        "spaces": {},
        "finSpaces": {"a": [],
                      "b": [],
                      "c": [],
                      "d": []}
    }

    for card in gameboard.deck:
        dict["deck"].append({"type": card.type, "value": card.value})

    for i in range(len(gameboard.spaces)):
        pile = gameboard.spaces[i]

        pileDict = {
            "shownCards": [],
            "hiddenCards": []
        }
        for card in pile.shownCards:
            pileDict["shownCards"].append({"type": card.type, "value": card.value})

        for card in pile.hiddenCards:
            pileDict["hiddenCards"].append({"type": card.type, "value": card.value})

        dict["spaces"][i] = pileDict

    for type in "a","b","c","d":
        dict["finSpaces"][type] = []
        for card in gameboard.finSpaces[type]:
            dict["finSpaces"][type].append({"type": card.type, "value": card.value})

    return dict

def gameboardDecoder(json):
    gameboard = Gameboard(0)  # setup a clean gameboard

    gameboard.deckPointer = json["deckPointer"]

    for card in json["deck"]:
        gameboard.deck.append(Card(card["type"], card["value"]))

    for i in range(len(json["spaces"])):

        pile = json["spaces"][str(i)]

        shownCards = []
        hiddenCards = []

        for card in pile["shownCards"]:
            shownCards.append(Card(card["type"], card["value"]))

        for card in pile["hiddenCards"]:
            hiddenCards.append(Card(card["type"], card["value"]))

        gameboard.spaces.append(Pile(shownCards, hiddenCards))

    for type in "a","b","c","d":
        for card in json["finSpaces"][type]:
            gameboard.finSpaces[type].append(Card(card["type"], card["value"]))

    return gameboard


class TurnGeneration(Resource):
    def post(self):
        gameboard = gameboardDecoder(request.get_json())
        check = SolitareChecker.checkSolitare(gameboard)
        if check != "OK":
            return {"correct": False, "msg": check}, 406  # Not acceptable
        else:
            command = AlgoChooser.eval_board(gameboard)
            instructions = InstructionConverter.convertInstructions(command, gameboard)
            return {"correct": True, "msg": instructions}, 200  # OK


class ImgRecon(Resource):
    def get(self):
        return render_template('upload.html')

    def post(self):
        now = datetime.now()
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save("img/" + now.strftime("%d_%m_%Y-%H_%M_%S"))
            return gameboardEncoder(Gameboard()), 200
        else:
            return {"Error": True}, 404


api.add_resource(TurnGeneration, '/turn/')
api.add_resource(ImgRecon, '/')


"""
@app.route('/',methods=['GET'])
def index():
   return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    now = datetime.now()
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(now.strftime("%d_%m_%Y-%H_%M_%S"))
        return jsonify("Board in her")
"""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")

