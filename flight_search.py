import os
from dotenv import load_dotenv
import requests as rq

load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:

    def __init__(self):
        self._api_key = os.environ['AMADEUS_API_KEY']
        self._api_secret = os.environ['AMADEUS_API_SECRET']
        self._token = self._get_new_token()

    # getting temporary token for flight search
    def _get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret,
        }
        response = rq.post(
            url=TOKEN_ENDPOINT,
            headers=header,
            data=body
        )
        token_detail = response.json()
        print(f"Your token will expire in {token_detail['expires_in']}")
        
        return token_detail['access_token']

    # getting iataCode for each city present in sheet
    def get_iata_code(self, city_name):
        headers = {'Authorization': f'Bearer {self._token}'}
        query = {
            'keyword': city_name,
            'max': 2,
            'include': 'AIRPORTS',
        }
        response = rq.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params=query
        )
        airport_details = response.json()
        try:
            iata_code = airport_details['data'][0]['iataCode']
        except IndexError:
            print(f"IndexError: No Airport code found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"KeyError: No Airport code found for {city_name}")
            return "No found"
        
        return iata_code

    def search_flights(self, origin_location_code: str, destination_code: str, departure_date, return_date, is_direct = True):
        headers = {'Authorization': f'Bearer {self._token}'}
        query = {
            'originLocationCode': origin_location_code,
            'destinationLocationCode': destination_code,
            'departureDate': f'{departure_date.strftime("%Y-%m-%d")}',
            'returnDate': f'{return_date.strftime("%Y-%m-%d")}',
            'adults': 1,
            'nonStop': 'true',
            'currencyCode': 'GBP',
            'max': 10,
        }
        response = rq.get(url=FLIGHT_ENDPOINT, params=query, headers=headers)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()
