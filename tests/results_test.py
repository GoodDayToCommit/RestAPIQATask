import json
import requests as re
from conftest import BaseClass
from support.mapping import *
from support.assertions import assert_valid_schema


class TestResults(BaseClass):
    def test_get_winners_history(self): ...

    def test_get_winners_from_future(self): ...

    def test_get_winners_from_past(self): ...

    def test_reset_current_data(self):
        # PRECONDITIONS
        name = "Taco Bell"
        rest_id = self.create_restaurant(name).json()["id"]
        self.vote_for(rest_id)
        polls = self.get_polls(today=True)
        assert {'id': rest_id, 'score': 4, 'voters': 1, 'name': name} in polls.json()["rankings"], \
            f"Restaurants was not appeared in rankings"

        # ACTION
        reset = self.reset_poll(today=True)
        polls = self.get_polls(today=True)
        assert reset.status_code == 200, f"Actual status code {reset.status_code}"
        assert {'id': rest_id, 'score': 4, 'voters': 1, 'name': name} not in polls.json()["rankings"], \
            f"Restaurants appeared in rankings"
        assert reset.json() == {'ok': True}, f"RESET: actual result {reset.json()}"

    def test_reset_data_from_future(self): ...

    def test_reset_data_from_past(self): ...
