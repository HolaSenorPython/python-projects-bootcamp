import requests
import os
from data_manager import DataManager
import datetime as dt
IATA_ENDP = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_SEARCH_ENDP = "https://test.api.amadeus.com/v2/shopping/flight-offers"
class FlightSearch(DataManager):
    def __init__(self):
        super().__init__()
        self.AMADEUS_API_KEY = os.environ['AMADEUS_KEY']
        self.AMADEUS_API_SECRET = os.environ['AMADEUS_SECRET']
        self.TOKEN_ENDPOINT = os.environ['AMA_TOKEN_ENDP']
        self._token = self._get_new_token()
        self.my_iata_code = "ATL"

    def _get_new_token(self):
        # Return token acquired after inputting api key and secret
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self.AMADEUS_API_KEY,
            "client_secret": self.AMADEUS_API_SECRET,
        }
        response = requests.post(url=self.TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()
        data = response.json()
        print(f"Amadeus Response Successful! Your token is: {data['access_token']}")
        print(f"Your token expires in: {data['expires_in']} seconds")
        return data['access_token']

    def get_iata_codes(self, city_name):
        # This will return the IATA code of the City in question in our sheet.
            print(f"Using Token: {self._token}")
            header = {"Authorization": f"Bearer {self._token}"}
            query = {
                "keyword": city_name,
                "max": "2",
                "include": "AIRPORTS",
            }
            response = requests.get(url=IATA_ENDP,params=query,headers=header)
            response.raise_for_status()
            data = response.json()
            print("Accessing IATA codes...")
            return data['data'][0]['iataCode']

    def flight_search(self, iata_code):
        # This will search for flights and return the json if it was successful, we will parse it in Flight Data
        today = dt.datetime.now().date()
        six_months_from_now = today + dt.timedelta(days=180)
        print(f"Using Token: {self._token}")
        header = {"Authorization": f"Bearer {self._token}"}
        flight_params = {
            "originLocationCode": self.my_iata_code,
            "destinationLocationCode": iata_code,
            "departureDate": str(today),
            "returnDate": str(six_months_from_now),
            "adults": 1,
            "currencyCode": "USD",
            "max": 10,
        }
        # Try getting the flights, if you get an error print something
        try:
            flight_s_response = requests.get(url=FLIGHT_SEARCH_ENDP,headers=header,params=flight_params)
            print("API Response:", flight_s_response.text)
            flight_s_response.raise_for_status()
            flight_data = flight_s_response.json()
            return flight_data
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Something went wrong: {err}")
