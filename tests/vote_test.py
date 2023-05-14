import json
import requests as re
from conftest import BaseClass
from support.mapping import *
from support.assertions import assert_valid_schema


class TestVote(BaseClass):
    def test_vote_for_existed_restaurant(self): ...

    def test_vote_for_not_existed_restaurant(self): ...
