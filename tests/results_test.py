import json

from conftest import BaseClass
from support.assertions import assert_valid_schema


class TestResults(BaseClass):
    def test_get_winners_history(self):
        # PRECONDITIONS
        self.new_user()
        date_from = "2023-01-01"
        date_to = "2023-05-17"

        # ACTION
        poll = self.get_polls(from_date=date_from, to_date=date_to)
        assert poll.status_code == 200, f"Status code: {poll.status_code}"

        json_data = json.loads(poll.content)
        assert_valid_schema(json_data, "polls_history.json")

    def test_get_winners_from_future(self):
        # PRECONDITIONS
        self.new_user()
        date_from = "2025-01-01"
        date_to = "2025-02-02"

        # ACTION
        poll = self.get_polls(from_date=date_from, to_date=date_to)
        assert poll.status_code == 400, f"Status code: {poll.status_code}"
        assert poll.json() == {'error': 'Invalid from or to dates'}

    def test_get_winners_from_past(self):
        # PRECONDITIONS
        self.new_user()
        date_from = "1900-01-01"
        date_to = "1910-05-17"

        # ACTION
        poll = self.get_polls(from_date=date_from, to_date=date_to)
        assert poll.status_code == 400, f"Status code: {poll.status_code}"
        assert poll.json() == {'error': 'Invalid from or to dates'}

    def test_reset_current_data(self):
        # PRECONDITIONS
        self.new_user()
        name = "Taco Bell"
        rest_id = self.create_restaurant(name).json()["id"]
        self.vote_for(rest_id)
        polls = self.get_polls(today=True)

        # ACTION
        assert {'id': rest_id, 'score': 4, 'voters': 1, 'name': name} in polls.json()["rankings"], \
            f"Restaurants was not appeared in rankings"
        reset = self.reset_poll(today=True)
        polls = self.get_polls(today=True)
        assert reset.status_code == 200, f"Actual status code {reset.status_code}"
        assert {'id': rest_id, 'score': 4, 'voters': 1, 'name': name} not in polls.json()["rankings"], \
            f"Restaurants appeared in rankings"
        assert reset.json() == {'ok': True}, f"RESET: actual result {reset.json()}"

    def test_reset_data_from_future(self):
        # PRECONDITIONS
        self.new_user()
        date = "2030-02-02"

        # ACTION
        reset = self.reset_poll(date=date)
        assert reset.status_code == 400, f"Status code: {reset.status_code}"
        assert reset.json() == {'error': 'Invalid from or to dates'}

    def test_reset_data_from_past(self):
        # PRECONDITIONS
        self.new_user()
        date = "1900-01-01"

        # ACTION
        reset = self.reset_poll(date=date)
        print(reset.json())
        assert reset.status_code == 400, f"Status code: {reset.status_code}"
        assert reset.json() == {'error': 'Invalid from or to dates'}
