import logging
from datetime import datetime

import pytest
import requests as re
from tests.support.mapping import *


class BaseClass:
    api_url = "https://convious-qa-homework.fly.dev/api/v1/"
    username = "AzamatImaevTheBestQAWorker"
    email = "azamat.imaev.work@gmail.com"
    password = "SuperSecretPassword"
    headers = {"Authorization": "Token 1464694b555cf8c0e92e7481d3d8022a17f55a6b"}

    def _get_token(self, username, email, password) -> str:
        """
        Create an authorization token for new user / if previous expired
        :return: token:str
        """
        headers = {"Content-Type": "application/json"}
        re.post(url=self.api_url + CREATE_USER,
                headers=headers, json={"username": username,
                                       "email": email,
                                       "password": password})
        get_token = re.post(url=self.api_url + GET_TOKEN,
                            headers=headers, json={"username": username,
                                                   "password": password})
        token = get_token.json()["auth_token"]
        logging.info(f"POST: token was created - {token}")
        return token

    def new_user(self, username, email, password):
        """
        Creates new user with new token
        """
        token = self._get_token(username=username, email=email, password=password)
        self.headers = {"Authorization": f"Token {token}"}
        return self.headers

    def get_restaurants(self):
        logging.info("GET: all restaurants")
        return re.get(self.api_url + RESTAURANTS, headers=self.headers)

    def create_restaurant(self, name):
        logging.info(f"POST: creating restaurant with name {name}")
        return re.post(self.api_url + RESTAURANTS,
                       headers=self.headers, json={"name": name})

    def change_restaurant(self, rest_id, new_name):
        logging.info(f"POST: changing restaurant with {rest_id} -> {new_name}")
        return re.put(self.api_url + RESTAURANTS + f"{rest_id}/",
                      headers=self.headers, json={"name": new_name})

    def delete(self, rest_id=0, all_rests=False):
        if all_rests:
            restaurants = re.get(self.api_url + RESTAURANTS, headers=self.headers).json()
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
