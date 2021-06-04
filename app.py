from flask import Flask, request
from flask_restful import Resource, Api
import turnGen.SolitareChecker as SolitareChecker
from turnGen.objects.Gameboard import Gameboard

app = Flask(__name__)
api = Api(app)


class TurnGeneration(Resource):
    def post(self):
        gameboard = request.get_json()
        return {"check": SolitareChecker.checkSolitare(gameboard)}, 201

    def get(self):
        return Gameboard()


api.add_resource(TurnGeneration, '/turn/')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
