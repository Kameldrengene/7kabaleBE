import io
from flask import json
from io import StringIO

import flask

from app import app
import unittest


class FlaskTestCase(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.dir = None

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)

    def test_picture(self):
        data =dict(
            file=(io.BytesIO(b"abcdef"), 'test.jpg')
        )
        tester = app.test_client(self)
        response = tester.post('/',
                                 content_type='multipart/form-data',
                                 data=data,
                                 follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_board(self):
        data =dict(
            file=(io.BytesIO(b"abcdef"), 'test.jpg')
        )
        tester = app.test_client(self)
        response = tester.post('/',
                                 content_type='multipart/form-data',
                                 data=data,
                                 follow_redirects=True)

        responsedata = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        assert responsedata["deckPointer"] == 1

    def test_Turn(self):
        data = json.dumps({'deckPointer': 1, 'finSpaceConverter': {'0': 'a', '1': 'b', '2': 'c', '3': 'd'}, 'deck': [{'type': 3, 'value': 10}, {'type': 0, 'value': 14}], 'spaces': {'0': {'shownCards': [{'type': 2, 'value': 4}], 'hiddenCards': []}, '1': {'shownCards': [{'type': 3, 'value': 12}], 'hiddenCards': [{'type': 0, 'value': 14}]}, '2': {'shownCards': [{'type': 0, 'value': 11}], 'hiddenCards': [{'type': 0, 'value': 14}, {'type': 0, 'value': 14}]}, '3': {'shownCards': [{'type': 3, 'value': 6}], 'hiddenCards': [{'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}]}, '4': {'shownCards': [{'type': 1, 'value': 10}], 'hiddenCards': [{'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}]}, '5': {'shownCards': [{'type': 0, 'value': 13}], 'hiddenCards': [{'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}]}, '6': {'shownCards': [{'type': 1, 'value': 3}], 'hiddenCards': [{'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}, {'type': 0, 'value': 14}]}}, 'finSpaces': {'0': [{'type': 0, 'value': 2}], '1': [{'type': 1, 'value': 1}], '2': [{'type': 2, 'value': 1}], '3': [{'type': 3, 'value': 3}]}})

        tester = app.test_client(self)
        response = tester.post('/turn/',
                                 content_type='application/json',
                                 data=data,
                                 )

        responsedata = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        assert responsedata['msg'] == 'Ryk Hjerter 3 oven på Klør 4.'


if __name__ == '__main__':
    unittest.main()
