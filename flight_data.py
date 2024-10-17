class FlightData:

    def __init__(self, lowest_price, origin, destination, departure_date, return_date, stops_num):
        self.price = lowest_price
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.stops = stops_num

# TODO 〰〰〰〰〰〰〰〰〰〰 Iterate through each result and finding cheapest flight 〰〰〰〰〰〰〰〰〰〰
def find_cheapest_flight(data, flight_type):
    if data is None or not data['data']:
        print(f"No {flight_type} flight found")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    # setup flight_detail from first result in given data
    first_flight = data['data'][0]
    lowest_price = float(first_flight['price']['grandTotal'])
    number_of_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    # destination is present in the last segment of first itinerary
    destination = first_flight["itineraries"][0]["segments"][number_of_stops]["arrival"]["iataCode"]
    departure_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    # Return_date present in the first segment of second itinerary
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
    cheapest_flight = FlightData(
        lowest_price,
        origin,
        destination,
        departure_date,
        return_date,
        number_of_stops
    )

    # setup cheap flight_detail by iterating
    for flight in data['data']:
        price = float(flight['price']['grandTotal'])
        if price < lowest_price:
            lowest_price = price
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][number_of_stops]["arrival"]["iataCode"]
            departure_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(
                lowest_price,
                origin,
                destination,
                departure_date,
                return_date,
                number_of_stops
            )
            print(f"lowest price to {destination} is £{lowest_price}")

    return cheapest_flight
