def find_cheapest_flight(data):
    # Parses the data we got from flight search / Amadeus API and makes use of it 😆

    # handles empty data
    if data is None or not data['data']:
        print("No flight data.")
        return FlightData("N/A","N/A","N/A","N/A","N/A")

    # First flight data in json
    first_flight = data['data'][0]
    lowest_price = float(first_flight['price']['grandTotal'])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][1]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    # Make a flight data object to compare
    cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)

    for flight in data['data']:
        price = float(flight['price']['grandTotal'])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][1]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date)
            print(f"Lowest price to {destination} is: ${lowest_price}")

    return cheapest_flight


class FlightData:
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        # Making a new flight data object with the corresponding details
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date

