import json
import requests as re
from conftest import BaseClass
from support.mapping import *
from support.assertions import assert_valid_schema


class TestRestaurants(BaseClass):
    def test_get_list_of_restaurants(self):
        # ACTION
        all_restaurants = re.get(self.api_url + RESTAURANTS, headers=self.headers)
        assert all_restaurants.status_code == 200, \
            f"GET: actual status code {all_restaurants.status_code}"

        json_data = json.loads(all_restaurants.content)
        assert_valid_schema(json_data, "all_restaurants.json")

    def test_create_restaurant(self):
        # PRECONDITIONS
        name = "Burger King"

        # ACTION
        create = self.create_restaurant(name)
        id_created = create.json()["id"]

        assert create.status_code == 201, \
            f"POST: actual status code {create.status_code}"
        all_restaurants = re.get(self.api_url + RESTAURANTS, headers=self.headers)
        assert {"id": id_created, "name": name} in all_restaurants.json()

        # POSTCONDITIONS
        self.delete(all_rest=True)

    def test_create_restaurant_with_null_name(self):
        # PRECONDITIONS
        name = None

        # ACTION
        create_restaurant = re.post(self.api_url + RESTAURANTS, headers=self.headers,
                                    json={"name": name})
        assert create_restaurant.status_code == 400, \
            f"POST: actual status code {create_restaurant.status_code}"
        assert create_restaurant.json()["name"] == ['This field may not be null.']

    def test_create_restaurant_with_int_name(self):
        # PRECONDITIONS
        name = 12345

        # ACTION
        create_restaurant = re.post(self.api_url + RESTAURANTS, headers=self.headers,
                                    json={"name": name})
        assert create_restaurant.status_code == 201, \
            f"POST: actual status code {create_restaurant.status_code}"
        id_created = create_restaurant.json()["id"]

        all_restaurants = re.get(self.api_url + RESTAURANTS, headers=self.headers)
        assert {"id": id_created, "name": str(name)} in all_restaurants.json()

        # POSTCONDITIONS
        re.delete(self.api_url + RESTAURANTS + f"{id_created}/",
                  headers=self.headers)

    def test_change_exist_restaurant(self):
        # PRECONDITIONS
        name = "Old boring name"
        new_name = "New cool name"
        create_restaurant = re.post(self.api_url + RESTAURANTS,
                                    headers=self.headers, json={"name": name})
        id_created = create_restaurant.json()["id"]

        # ACTION
        change_restaurant = re.put(self.api_url + RESTAURANTS + f"{id_created}/",
                                   headers=self.headers,
                                   json={"name": new_name})
        assert change_restaurant.status_code == 200, \
            f"PUT: actual status code {change_restaurant.status_code}"
        id_created = change_restaurant.json()["id"]

        all_restaurants = re.get(self.api_url + RESTAURANTS, headers=self.headers)
        assert {"id": id_created, "name": new_name} in all_restaurants.json()

        # POSTCONDITIONS
        re.delete(self.api_url + RESTAURANTS + f"{id_created}/",
                  headers=self.headers)

    def test_change_not_existed_restaurant(self):
        # PRECONDITIONS
        new_id = 123456677

        # ACTION
        change_restaurant = re.put(self.api_url + RESTAURANTS + f"{new_id}/",
                                   headers=self.headers,
                                   json={"name": "Not existed name"})
        assert change_restaurant.status_code == 404, \
            f"PUT: actual status code {change_restaurant.status_code}"

    def test_delete_restaurant(self):
        # PRECONDITIONS
        name = "Burger King"
        id_created = self.create_restaurant(name).json()["id"]

        # ACTION
        delete_restaurant = re.delete(self.api_url + RESTAURANTS + f"{id_created}/",
                                      headers=self.headers)
        assert delete_restaurant.status_code == 204, \
            f"DELETE: actual status code {delete_restaurant.status_code}"
        all_restaurants = re.get(self.api_url + RESTAURANTS, headers=self.headers)
        assert {"id": id_created, "name": name} not in all_restaurants.json()

    def test_delete_not_existed_restaurant(self):
        # PRECONDITIONS
        new_id = 12312312

        # ACTION
        delete_restaurant = re.delete(self.api_url + RESTAURANTS + f"{new_id}/",
                                      headers=self.headers)
        assert delete_restaurant.status_code == 404, \
            f"DELETE: actual status code {delete_restaurant.status_code}"
