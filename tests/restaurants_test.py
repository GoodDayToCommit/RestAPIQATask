import json
import requests as re
from conftest import BaseClass
from support.mapping import *
from support.assertions import assert_valid_schema


class TestRestaurants(BaseClass):
    def test_get_list_of_restaurants(self): ...

    def test_create_restaurant(self): ...

    def test_create_restaurant_without_name(self): ...

    def test_change_exist_restaurant(self): ...

    def test_change_not_existed_restaurant(self): ...

    def test_delete_restaurant(self): ...

    def test_delete_not_existed_restaurant(self): ...