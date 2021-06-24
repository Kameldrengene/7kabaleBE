# !flask/bin/python
# Frederik Koefoed s195463
# Lasse Strunge s195486
# Mark Mortensen s174881
# Mikkel Danielsen s183913
# Muhammad Talha s195475
# Volkan Isik s180103

from flask import *
from flask_restful import Resource, Api
from datetime import datetime
from turnGen.objects.Gameboard import Gameboard
from turnGen.objects.Gameboard import Card
from turnGen.objects.Gameboard import Pile
import turnGen.SolitareChecker as SolitareChecker
import turnGen.InstructionConverter as InstructionConverter
import turnGen.AlgoChooser as AlgoChooser
import ImageRecognition.detectCards as Detector
import turnGen.BoardConverter as BoardConverter

app = Flask(__name__)
api = Api(app)

def gameboardEncoder(gameboard):
    """
    * Encoder serializes the Gameboard object
    * works by manually setting up the Gameboard object as a dictionary
    """

    # initial spots for serialization
    # deckPointer and finSpaceConverter are instantly serializable
    dict = {
        "deckPointer": gameboard.deckPointer,
        "finSpaceConverter": gameboard.finSpaceConverter,
        "deck": [],
        "spaces": {},
        "finSpaces": {0: [],
                      1: [],
                      2: [],
                      3: []}
    }

    # add all cards in gameboard.deck to the list
    for card in gameboard.deck:
        dict["deck"].append({"type": card.type, "value": card.value})

    # serialize each pile one at a time
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

        # Adding the serialized pile
        dict["spaces"][i] = pileDict

    # Adding all finSpaces
    for type in range(4):
        dict["finSpaces"][type] = []
        for card in gameboard.finSpaces[gameboard.finSpaceConverter[type]]:
            dict["finSpaces"][type].append({"type": card.type, "value": card.value})

    return dict

def gameboardDecoder(json):
    """
    * Decoder unserializes the Gameboard object
    * works by manually setting up the Gameboard object with the values of the Json dictionary
    """

    gameboard = Gameboard(0)  # setup a clean gameboard

    print(json["deck"])

    # setting deck
    for card in json["deck"]:
        gameboard.deck.append(Card(card["type"], card["value"]))

    # deckpointer
    if len(gameboard.deck) == 0:
        gameboard.deckPointer = -1
    elif gameboard.deck[0].value == 14:
        gameboard.deckPointer = -1
    elif gameboard.deck[0].value == 0:
        gameboard.deckPointer = -1
    else:
        gameboard.deckPointer = 0

    #print(gameboard.deck[gameboard.deck)
    # setting spaces
    for i in range(len(json["spaces"])):

        pile = json["spaces"][str(i)]

        shownCards = []
        hiddenCards = []

        for card in pile["shownCards"]:
            shownCards.append(Card(card["type"], card["value"]))

        for card in pile["hiddenCards"]:
            hiddenCards.append(Card(card["type"], card["value"]))

        gameboard.spaces.append(Pile(shownCards, hiddenCards))

    # setting the finSpaces
    for type in range(4):
        for card in json["finSpaces"][str(type)]:
            gameboard.finSpaces[gameboard.finSpaceConverter[type]].append(Card(card["type"], card["value"]))

    return gameboard


class TurnGeneration(Resource):
    def get(self):
        # testing gameboard
        gameboard = Gameboard()
        return gameboard

    def post(self):
        """
        * recives a gameboad in Json
        * Decodes the gameboard
        * checks the gamboard to see if it is legal
        * returns either a false boolean and a error message
        * or a true boolean and instructions for the next move
        """
        gameboard = gameboardDecoder(request.get_json())
        BoardConverter.convertBoard(gameboard)
        check = SolitareChecker.checkSolitare(gameboard)
        if check != "OK":
            # The gameboard is illegal
            # setting the json return to have charset utf8 for acommadate the danish language
            json_string = json.dumps({"correct": False, "msg": check}, ensure_ascii=False)
            response = Response(json_string, content_type="application/json; charset=utf-8")
            return response
        else:
            # the gameboard is legal
            # Algochooser evaluating the board for the best instruction sequence
            command = AlgoChooser.eval_board(gameboard)

            # converting the instructions found to readable danish
            instructions = InstructionConverter.convertInstructions(command, gameboard)

            # setting the json return to have charset utf8 for acommadate the danish language
            json_string = json.dumps({"correct": True, "msg": instructions}, ensure_ascii=False)
            response = Response(json_string, content_type="application/json; charset=utf-8")
            return response


class ImgRecon(Resource):
    def get(self):
        return render_template('upload.html')

    def post(self):
        now = datetime.now()
        # retrieving the image sent from App
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save("img/" + now.strftime("%d_%m_%Y-%H_%M_%S.jpg"))

            # temp returning a new gameboard object.
            detectorObj = Detector.Detector()
            #gameboard = detectorObj.detectSolitaire("/home/cdio/syvkabale/syvkabaleBE/img/1.jpg")
            gameboard = detectorObj.detectSolitaire("/home/cdio/syvkabale/syvkabaleBE/img/"+now.strftime("%d_%m_%Y-%H_%M_%S.jpg"))
            # gameboard = detector.detectSolitaire(detectorObj,"../img/"+now.strftime("%d_%m_%Y-%H_%M_%S.jpg"))
            # gameboard = Gameboard()
            # for pile in gameboard.spaces:
            #     for card in pile.hiddenCards:
            #         card.value = 14
            return gameboardEncoder(gameboard), 200
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
    app.run(host="0.0.0.0", port="5000", debug=True)

