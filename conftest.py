import allure
import logging
import requests as re
from datetime import datetime
from src.support.logger import log
from src.support.mapping import *
from random_username.generate import generate_username


class BaseClass:
    """
    In this specified all needed parameters and methods needed
    for steps in autotests
    """
    api_url = ""
    username: str
    email: str
    password: str
    _headers = {"Content-Type": "application/json"}
    _timeout = 10
    response = None

    def get(self):
        ...

    @allure.step("Sending POST request")
    def post(self, url: str, endpoint: str, json_body: dict = None):
        with allure.step(f"POST request for: {url}{endpoint} with body: \n {json_body}"):
            self.response = re.post(url=f"{url}{endpoint}",
                                    headers=self._headers,
                                    json=json_body,
                                    timeout=self._timeout)
        log(response=self.response, request_body=json_body)

        return self

    @allure.step("Sending PUT request")
    def put(self):
        ...

    @allure.step("Sending DELETE request")
    def delete(self):
        ...

    @allure.step("Status code is {expected_code}")
    def check_status_code(self, expected_code: int):
        actual_code = self.response.status_code
        assert expected_code == actual_code, f"ER: {expected_code}, AR: {actual_code}"

        return self

    def _get_token(self) -> str:
        """
        Create an authorization token for new user / if previous expired
        :return: token:str
        """
        re.post(url=self.api_url + CREATE_USER,
                headers=self._headers, json={"username": self.username,
                                             "email": self.email,
                                             "password": self.password})
        get_token = re.post(url=self.api_url + GET_TOKEN,
                            headers=self._headers, json={"username": self.username,
                                                         "password": self.password})
        token = get_token.json()["auth_token"]
        logging.info(f"POST: token was created - {token}")
        return token

    def new_user(self):
        """ Creates new user using generator with a new token """
        self.username = generate_username(1)[0]
        self.email = (self.username + "@gmail.com")
        self.password = generate_username(1)[0]  # To avoid error "password is too similar to the username"
        token = self._get_token()
        self._headers = {"Authorization": f"Token {token}"}
        logging.info("New user created")
        return self._headers, self.username, self.email, self.password

    def get_restaurants(self):
        logging.info("GET: all restaurants")
        return re.get(self.api_url + RESTAURANTS, headers=self._headers)

    def create_restaurant(self, name):
        logging.info(f"POST: creating restaurant with name {name}")
        return re.post(self.api_url + RESTAURANTS,
                       headers=self._headers, json={"name": name})

    def change_restaurant(self, rest_id, new_name):
        logging.info(f"POST: changing restaurant with {rest_id} -> {new_name}")
        return re.put(self.api_url + RESTAURANTS + f"{rest_id}/",
                      headers=self._headers, json={"name": new_name})

    def delete(self, rest_id=0, all_rests=False):
        if all_rests:
            restaurants = re.get(self.api_url + RESTAURANTS, headers=self._headers).json()
            if len(restaurants) > 0:
                for rest in restaurants:
                    re.delete(self.api_url + RESTAURANTS + f"{rest['id']}/", headers=self.headers)
                    logging.info(f"DELETE: restaurant with id '{rest['id']}'")

        else:
            logging.info(f"DELETE: restaurant with id '{rest_id}'")
            return re.delete(self.api_url + RESTAURANTS + f"{rest_id}/", headers=self.headers)

    def get_polls(self, today=False, from_date="", to_date=""):
        if today:
            logging.info("GET: today's polls")
            return re.get(self.api_url + POLLS_TODAY, headers=self.headers)
        else:
            logging.info(f"GET: results of polls for {from_date} to {to_date}")
            return re.get(self.api_url + POLLS_BY_DATE.format(FROM=from_date, TO=to_date), headers=self.headers)

    def vote_for(self, rest_id):
        return re.post(self.api_url + VOTE, headers=self.headers, json={"restaurant_id": rest_id})

    def reset_poll(self, date="2023-01-01", today=False):
        if today:
            now = datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            return re.post(self.api_url + RESET, headers=self.headers, json={"date": current_date})
        else:
            return re.post(self.api_url + RESET, headers=self.headers, json={"date": date})
