import json
from conftest import BaseClass
from src.support.assertions import assert_valid_schema


class TestRestaurants(BaseClass):
    def test_get_list_of_restaurants(self):
        # PRECONDITIONS
        self.new_user()
        self.create_restaurant("MacDonald's")
        self.create_restaurant("PizzaHut")
        self.create_restaurant("KFC")

        # ACTION
        restaurants = self.get_restaurants()
        assert restaurants.status_code == 200, \
            f"GET: status code {restaurants.status_code}"

        json_data = json.loads(restaurants.content)
        assert_valid_schema(json_data, "all_restaurants.json")

        # POSTCONDITIONS
        self.delete(all_rests=True)

    def test_get_empty_list_of_restaurants(self):
        # PRECONDITION
        self.new_user()
        self.delete(all_rests=True)

        # ACTION
        restaurants = self.get_restaurants()
        assert restaurants.status_code == 200, \
            f"GET: status code {restaurants.status_code}"

        json_data = json.loads(restaurants.content)
        assert_valid_schema(json_data, "all_restaurants.json")

    def test_create_restaurant(self):
        # PRECONDITIONS
        self.new_user()
        name = "Burger King"

        # ACTION
        create = self.create_restaurant(name)
        id_created = create.json()["id"]

        assert create.status_code == 201, \
            f"POST: status code {create.status_code}"
        restaurants = self.get_restaurants()
        assert {"id": id_created, "name": name} in restaurants.json()

        # POSTCONDITIONS
        self.delete(all_rests=True)

    def test_create_restaurant_with_null_name(self):
        # PRECONDITIONS
        self.new_user()
        name = None

        # ACTION
        create = self.create_restaurant(name)

        assert create.status_code == 400, \
            f"POST: status code {create.status_code}"
        assert create.json()["name"] == ['This field may not be null.'], \
            f"CREATE: no error for None named restaurant"

    def test_create_restaurant_with_int_name(self):
        # PRECONDITIONS
        self.new_user()
        name = 12345

        # ACTION
        create = self.create_restaurant(name)

        assert create.status_code == 201, \
            f"POST: actual status code {create.status_code}"
        id_created = create.json()["id"]

        restaurants = self.get_restaurants()
        assert {"id": id_created, "name": str(name)} in restaurants.json()

        # POSTCONDITIONS
        self.delete(all_rests=True)

    def test_change_restaurant_name(self):
        # PRECONDITIONS
        self.new_user()
        name = "Old boring name"
        new_name = "New cool name"
        create = self.create_restaurant(name)
        id_created = create.json()["id"]

        # ACTION
        change = self.change_restaurant(rest_id=id_created, new_name=new_name)

        assert change.status_code == 200, \
            f"PUT: actual status code {change.status_code}"

        restaurants = self.get_restaurants()
        assert {"id": id_created, "name": new_name} in restaurants.json()

        # POSTCONDITIONS
        self.delete(all_rests=True)

    def test_change_not_existed_restaurant(self):
        # PRECONDITIONS
        self.new_user()
        new_id = 123456677

        # ACTION
        change = self.change_restaurant(rest_id=new_id, new_name="Not existed name")

        assert change.status_code == 404, \
            f"PUT: actual status code {change.status_code}"

    def test_delete_restaurant(self):
        # PRECONDITIONS
        self.new_user()
        name = "Burger King"
        id_created = self.create_restaurant(name).json()["id"]

        # ACTION
        delete = self.delete(rest_id=id_created)

        assert delete.status_code == 204, \
            f"DELETE: actual status code {delete.status_code}"
        restaurants = self.get_restaurants()
        assert {"id": id_created, "name": name} not in restaurants.json()

    def test_delete_not_existed_restaurant(self):
        # PRECONDITIONS
        self.new_user()
        new_id = 12312312

        # ACTION
        delete = self.delete(rest_id=new_id)
        assert delete.status_code == 404, \
            f"DELETE: actual status code {delete.status_code}"
