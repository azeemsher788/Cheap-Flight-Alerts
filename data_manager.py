import os
import requests as rq
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

SHEETY_PRICES_ENDPOINT = os.environ['SHEETY_ENDPOINT']
SHEETY_CUSTOMER_ENDPOINT = os.environ['SHEETY_CUSTOMER_ENDPOINT']


class DataManager:

    def __init__(self):
        self._username = os.environ['SHEETY_USERNAME']
        self._password = os.environ['SHEETY_PASSWORD']
        self._auth = HTTPBasicAuth(
            username=self._username,
            password=self._password
        )
        self.sheet_data = {}

    def get_sheet_data(self):
        response = rq.get(
            url=SHEETY_PRICES_ENDPOINT,
            auth=self._auth
        )
        self.sheet_data = response.json()

        return self.sheet_data['prices']

    def get_customer_data(self):
        response = rq.get(
            url=SHEETY_CUSTOMER_ENDPOINT,
            auth=self._auth
        )
        self.sheet_data = response.json()

        return self.sheet_data['users']

    def update_sheet_data(self, row_id, iata_code):
        new_data = {
            "price": {
                "iataCode": iata_code
            }
        }
        response = rq.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{row_id}",
            auth=self._auth,
            json=new_data
        )
        print(response.text)

