#This file will need to use the DataManager, FlightSearch,
# FlightData, NotificationManager classes to achieve the program requirements.
from dotenv import load_dotenv
import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
load_dotenv()

data_manager = DataManager()
flight_search = FlightSearch()

# Check if there's IATA codes in the sheet, if NOT add them
sheet_data = data_manager.data["atlantaFlightPricesUpdatedCsv"]
for row in sheet_data:
    ID = row["id"]
    code = flight_search.get_iata_codes(row['city'])
    if row['iataCode'] == '':
        data_manager.place_iata_codes(ID, code)
        time.sleep(1)
    else:
        print("This row already has an IATA code.")
sheet_data = data_manager.data["atlantaFlightPricesUpdatedCsv"]
print(sheet_data)
# Search for Flights!
for row_again in sheet_data:
    print(f"Getting flights for {row_again['city']}...")
    flights = flight_search.flight_search(row_again['city'])
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{row_again['city']}: ${cheapest_flight.price}")