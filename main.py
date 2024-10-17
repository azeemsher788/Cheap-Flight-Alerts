from time import sleep
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import send_email

ORIGIN_CITY_CODE = "LON"
departure_date = datetime.now() + timedelta(days=1) # Tomorrow
return_date = departure_date + timedelta(days=(6*30)) # six months later

# TODO 〰〰〰〰〰〰〰〰〰〰 Setup objects from classes 〰〰〰〰〰〰〰〰〰〰
# Please add all of the required keys and values in .env file
data_manager = DataManager()
sheet_data = data_manager.get_sheet_data()
flight_search = FlightSearch()


# TODO 〰〰〰〰〰〰〰〰〰〰 Updating the sheet data 〰〰〰〰〰〰〰〰〰〰
for row in sheet_data:
    if row['iataCode'] == '':
        iata_Code =  flight_search.get_iata_code(row['city'])
        data_manager.update_sheet_data(row['id'], iata_Code)

sheet_data = data_manager.get_sheet_data() # Again getting as data updated
customer_data = data_manager.get_customer_data()
customer_data_dic = {f"{data['firstName']} {data['lastName']}": data['email'] for data in customer_data}

# TODO 〰〰〰〰〰〰〰〰〰〰 Searching cheapest flight and sending mail 〰〰〰〰〰〰〰〰〰〰

for city_detail in sheet_data:
    print(f"Getting flights for city {city_detail['city']}")
    direct_flights_result = flight_search.search_flights(
        ORIGIN_CITY_CODE,
        city_detail['iataCode'],
        departure_date,
        return_date
    )
    cheapest_flight = find_cheapest_flight(direct_flights_result, flight_type="direct")
    sleep(1) # To prevent rate limit
    if cheapest_flight.price == "N/A":
        indirect_flights_result = flight_search.search_flights(
            ORIGIN_CITY_CODE,
            city_detail['iataCode'],
            departure_date,
            return_date,
            is_direct="false",
        )
        cheapest_flight = find_cheapest_flight(indirect_flights_result, flight_type="indirect")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < city_detail['lowestPrice']:
        for (name, email) in customer_data_dic.items():
            if cheapest_flight.stops > 0:
                send_email(
                    message=f"Subject:Flight Alert!\n\n"
                    f"Hi {name} surprisingly on {cheapest_flight.departure_date} an"
                    f" indirect cheap flight is available"
                    f" to {city_detail['city']} with amount "
                    f"of £{cheapest_flight.price} with {cheapest_flight.stops} number of stops",
                    to_email=email,
                )
                print(f"Mail sent to {name} successfully")
            else:
                send_email(
                    message=f"Subject:Flight Alert!\n\n"
                            f"Hi {name} surprisingly on {cheapest_flight.departure_date} a"
                            f" direct cheap flight is available"
                            f" to {city_detail['city']} with amount of £{cheapest_flight.price}",
                    to_email=email,
                )
                print(f"Mail sent to {name} successfully")



