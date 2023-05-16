import pytest
import logging
import requests as re
from tests.support.mapping import *


class BaseClass:
    api_url = "https://convious-qa-homework.fly.dev/api/v1/"
    username = "AzamatImaevTheBestQAWorker"
    email = "azamat.imaev.work@gmail.com"
    password = "SuperSecretPassword"
    headers = {"Authorization": "Token 1464694b555cf8c0e92e7481d3d8022a17f55a6b"}

    def _get_token(self) -> str:
        """
        Function need to create an authorization token if previous one is expired
        :return: token:str
        """
        headers = {"Content-Type": "application/json"}
        re.post(url=self.api_url + CREATE_USER,
                headers=headers, data={"username": self.username,
                                       "email": self.email,
                                       "password": self.password})
        get_token = re.post(url=self.api_url + GET_TOKEN,
                            headers=headers, data={"username": self.username,
                                                   "password": self.password})
        self.auth_token = get_token.json()["auth_token"]
        logging.info(f"POST: token was created - {self.auth_token}")
        return self.auth_token

    def create_restaurant(self, name: str):
        logging.info("POST: creating restaurant")
        return re.post(self.api_url + RESTAURANTS,
                       headers=self.headers, json={"name": name})

    def delete(self, rest_id=0, all_rest=False):
        if all_rest:
            restaurants = re.get(self.api_url + RESTAURANTS, headers=self.headers).json()
            if len(restaurants) > 0:
                for rest in restaurants:
                    re.delete(self.api_url + RESTAURANTS + f"{rest['id']}/", headers=self.headers)
                    logging.info(f"DELETE: restaurant with id '{rest['id']}'")

        else:
            re.delete(self.api_url + RESTAURANTS + f"{rest_id}/", headers=self.headers)
            logging.info(f"DELETE: restaurant with id '{rest_id}'")
