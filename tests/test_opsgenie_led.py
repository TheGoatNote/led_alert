"""
Testing suite for opsgenie_led
"""

import os
import requests
from opsgenie_led import get_alert_list, parse_return_data

def test_get_alert_list():
    """
    We ensure that we get "data" when calling api
    """

    assert "data" in get_alert_list()

def test_parse_return_data(monkeypatch):
    """
    We push one result in data dict
    """

    results = {
            "data": [{
                "priority": "P3",
                "message": "My beautiful alert code"
                }]

          }

    class MockResponse(object):
        """
        We init an object to get a fake response
        """
        def __init__(self):
            """
            We init a small object
            """
            self.status_code = 200
            self.url = 'http://fakeurl.com'
            self.headers = '{fake: header}'

        def json(self):
            """
            We parse a json
            """
            return results

    def mock_get(url, headers):
        """
        And we fake a request get
        """
        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    assert get_alert_list()["data"][0]["priority"] == 'P3'
    assert parse_return_data() == True
