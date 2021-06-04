from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
import turnGen.SolitareChecker as SolitareChecker
from turnGen.objects.Gameboard import Gameboard

app = Flask(__name__)
api = Api(app)

card_fields = {
    "type": fields.Integer,
    "value": fields.Integer
}

pile_fields = {
    "shownCards": fields.List(card_fields),
    "hiddenCards": fields.List(card_fields)
}

gameboard_fields = {
    "dekpointer": fields.Integer,
    "deck": fields.List(card_fields),
    "spaces": fields.List(pile_fields),
}

gameboard_fields["finSpaces"]["a"] = fields.List(card_fields, attribute="a")
gameboard_fields["finSpaces"]["b"] = fields.List(card_fields, attribute="b")
gameboard_fields["finSpaces"]["c"] = fields.List(card_fields, attribute="c")
gameboard_fields["finSpaces"]["d"] = fields.List(card_fields, attribute="d")

gameboard_fields["finSpaceConverter"]["0"] = fields.String(attribute="0")
gameboard_fields["finSpaceConverter"]["1"] = fields.String(attribute="1")
gameboard_fields["finSpaceConverter"]["2"] = fields.String(attribute="2")
gameboard_fields["finSpaceConverter"]["3"] = fields.String(attribute="3")

class TurnGeneration(Resource):
    def post(self):
        gameboard = request.get_json()
        return {"check": SolitareChecker.checkSolitare(gameboard)}, 201

    @marshal_with(gameboard_fields)
    def get(self):
        return Gameboard()


api.add_resource(TurnGeneration, '/turn/')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
