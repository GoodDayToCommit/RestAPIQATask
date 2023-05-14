import pytest
import requests as re
from tests.support.mapping import *


class BaseClass:
    api_url = "https://convious-qa-homework.fly.dev/api/v1/"
    username = "AzamatImaevTheBestQAWorker"
    email = "azamat.imaev.work@gmail.com"
    password = "SuperSecretPassword"
    auth_token: str

    @pytest.fixture(scope="session")
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
        return self.auth_token
