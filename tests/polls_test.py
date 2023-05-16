import json
import requests as re
from conftest import BaseClass
from support.mapping import *
from support.assertions import assert_valid_schema


class TestPoll(BaseClass):
    def test_get_poll_status(self):
        response = re.get(self.api_url + POLLS_TODAY)
        assert response.status_code == 200, f"Status code: {response.status_code}"

        json_data = json.loads(response.content)
        assert_valid_schema(json_data, "poll_status.json")

    def test_get_poll_same_score(self): ...

    def test_get_poll_same_score_and_voters(self): ...

    def test_get_poll_one_participant(self): ...

    def test_get_poll_no_participants(self): ...

    def test_get_poll_after_change_name(self): ...

    def test_vote_for_five_restaurants(self): ...

    def test_vote_for_sixth_restaurant(self): ...

    def test_vote_for_existed_restaurant(self): ...

    def test_vote_for_not_existed_restaurant(self): ...
