import requests
import os
class DataManager:
    def __init__(self):
        self.SHEETY_ENDPOINT = os.environ['SHEETY_ENDP']
        self.SHEETY_AUTH = os.environ['SHEETY_AUTH']
        self.sheety_headers = {
            "Authorization": self.SHEETY_AUTH
        }
        self.data = None
        self.get_sheet()

    def get_sheet(self):
        # Get the sheet
        response = requests.get(url=self.SHEETY_ENDPOINT, headers=self.sheety_headers)
        response.raise_for_status()
        self.data = response.json()
        print("Google sheet successfully accessed!")

    def place_iata_codes(self, id_of_row, iata_code):
        # Place the IATA codes you got from flight search into the sheet with the code here!
        new_row_data = {
            "atlantaFlightPricesUpdatedCsv": {
                "iataCode": iata_code,
            }
        }
        response2 = requests.put(url=f"{self.SHEETY_ENDPOINT}/{id_of_row}", headers=self.sheety_headers,
                                json=new_row_data)
        response2.raise_for_status()
        self.data = response2.json()
        print("Placing IATA codes in Google Sheet....")