import json
import requests as re
from conftest import BaseClass
from support.mapping import *
from support.assertions import assert_valid_schema


class TestPoll(BaseClass):
    def test_get_poll_status(self):
        # ACTION
        poll = self.get_polls(today=True)
        assert poll.status_code == 200, f"Status code: {poll.status_code}"

        json_data = json.loads(poll.content)
        assert_valid_schema(json_data, "poll_status.json")

    def test_vote_for_restaurant(self):
        # PRECONDITIONS
        rest_id = self.create_restaurant("Taco Bell").json()["id"]

        # ACTION
        vote = self.vote_for(rest_id)

        json_data = json.loads(vote.content)
        assert_valid_schema(json_data, "vote.json")

        assert vote.json()["top"]["id"] == rest_id, \
            f"VOTE: restaurant did not get into the top"

        # POSTCONDITIONS
        self.reset_poll(today=True)

    def test_vote_for_five_restaurants_same_user(self):
        # PRECONDITIONS
        rest_id_1 = self.create_restaurant("Subway").json()["id"]
        rest_id_2 = self.create_restaurant("Burger King").json()["id"]
        rest_id_3 = self.create_restaurant("MacDonald's").json()["id"]
        rest_id_4 = self.create_restaurant("KFC").json()["id"]
        rest_id_5 = self.create_restaurant("Pizza Hut").json()["id"]

        # ACTION
        self.vote_for(rest_id_1)
        self.vote_for(rest_id_2)
        self.vote_for(rest_id_3)
        self.vote_for(rest_id_4)
        vote = self.vote_for(rest_id_5)

        assert vote.json()["top"]["id"] == rest_id_1, \
            f"VOTE: restaurant did not get into the top"
        assert vote.json()["rankings"][0]["id"] == rest_id_1
        assert vote.json()["rankings"][1]["id"] == rest_id_2
        assert vote.json()["rankings"][2]["id"] == rest_id_3
        assert vote.json()["rankings"][3]["id"] == rest_id_4
        assert vote.json()["rankings"][4]["id"] == rest_id_5

        # POSTCONDITIONS
        self.reset_poll(today=True)

    def test_vote_for_sixth_restaurant(self):
        # PRECONDITIONS
        rest_id_1 = self.create_restaurant("Subway").json()["id"]
        rest_id_2 = self.create_restaurant("Burger King").json()["id"]
        rest_id_3 = self.create_restaurant("MacDonald's").json()["id"]
        rest_id_4 = self.create_restaurant("KFC").json()["id"]
        rest_id_5 = self.create_restaurant("Pizza Hut").json()["id"]
        rest_id_6 = self.create_restaurant("Domino's").json()["id"]

        # ACTION
        self.vote_for(rest_id_1)
        self.vote_for(rest_id_2)
        self.vote_for(rest_id_3)
        self.vote_for(rest_id_4)
        self.vote_for(rest_id_5)
        vote = self.vote_for(rest_id_6)

        assert vote.status_code == 400, f"Status code: {vote.status_code}"
        assert vote.json() == {'error': 'Votes per day exceeded'}, f"No error for 6th vote"

        # POSTCONDITIONS
        self.reset_poll(today=True)

    def test_get_poll_same_score_diff_voters(self):
        # PRECONDITIONS
        self.reset_poll(today=True)

        rest_id_1 = self.create_restaurant("KFC").json()["id"]  # new rest to decrease vote amount for user#1
        rest_id_2 = self.create_restaurant("Taco Bell").json()["id"]  # new rest to decrease vote amount for user#2

        rest_id_3 = self.create_restaurant("Starbucks").json()["id"]  # will be voted for 4 points by user#3
        rest_id_4 = self.create_restaurant("Coffe Nero").json()["id"]  # will be voted for 2+2 points by user#1/#2

        # ACTION
        self.vote_for(rest_id_1)  # user#1 assigned 4 points to rest#1
        self.vote_for(rest_id_4)  # user#1 assigned 2 points to rest#4

        self.new_user(username="UserTwo", email="UserTwo@gmail.com", password="PasswordTwo")  # creating user #2
        self.vote_for(rest_id_2)  # user#2 assigned 4 points to rest#2
        self.vote_for(rest_id_4)  # user#2 assigned 2 points to rest#4

        self.new_user(username="UserThree", email="UserThree@gmail.com", password="PasswordThree")  # creating user #3
        vote = self.vote_for(rest_id_3)  # user#2 assigned 4 points to rest#3

        # total score: Starbucks - 4 points (1 voter), Coffee Nero (winner) - 4 points (2 voters)
        assert vote.json()["top"] == {'id': rest_id_4, 'score': 4, 'voters': 2, 'name': 'Coffe Nero'}, \
            f"VOTE: in case with same same score but different number of voters something wrong"

        # POSTCONDITIONS
        self.reset_poll(today=True)

    def test_get_poll_same_score_and_voters(self):
        # PRECONDITIONS
        self.reset_poll(today=True)
        rest_id_1 = self.create_restaurant("MacDonald's").json()["id"]
        rest_id_2 = self.create_restaurant("Subway").json()["id"]

        # ACTION
        self.vote_for(rest_id_1)  # user#1 assigned 4 points to rest#1

        self.new_user(username="SuperDuper", email="SuperDuper@gmail.com", password="Super1Pass123")  # user#2
        vote = self.vote_for(rest_id_2)  # user#2 assigned 4 points to rest#2

        assert vote.json()["top"] == {'id': rest_id_1, 'score': 4, 'voters': 1, 'name': "MacDonald's"}, \
            f"VOTE: winner {vote.json()['top']}"

        # POSTCONDITIONS
        self.reset_poll(today=True)

    def test_get_poll_one_participant(self):
        # PRECONDITIONS
        self.reset_poll(today=True)

        # ACTION
        poll = self.get_polls(today=True)
        assert poll.status_code == 200, f"Status code: {poll.status_code}"
        print(poll.json())

        json_data = json.loads(poll.content)
        assert_valid_schema(json_data, "poll_status.json")

    def test_get_poll_no_participants(self): ...

    def test_get_poll_after_change_name(self): ...

    def test_vote_for_not_existed_restaurant(self): ...
