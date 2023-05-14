import json
import requests as re
from conftest import BaseClass
from support.mapping import *
from support.assertions import assert_valid_schema


class TestPoll(BaseClass):
    def test_get_todays_poll_status(self):
        response = re.get(self.api_url + POLLS_TODAY)
        assert response.status_code == 200, f"Status code: {response.status_code}"

        json_data = json.loads(response.content)
        assert_valid_schema(json_data, "poll_status.json")

    def test_get_todays_poll_status_no_results(self): ...
