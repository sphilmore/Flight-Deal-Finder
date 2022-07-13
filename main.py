#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
import requests
from twilio.rest import Client
from data_manager import DataManager
from flight_search import FlightSearch
data_manager = DataManager()
flight_search=FlightSearch()
sheet_data = data_manager.get_destination_data()
ORIGIN_CITY_IATA = 'LON'
ACCOUNT = os.getenv('twilio_account')
TOKEN = os.getenv('twilio_token')
NUMBER = os.getenv('phone_number')
if sheet_data[0]['iataCode']== '':
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row['city'])
    data_manager.destination = sheet_data
    data_manager.update_code()


for destination in sheet_data:
     flight = flight_search.flight_info(
        "LON",
        destination['iataCode'],
     )
     if flight.price < destination['lowestPrice']:
        client = Client(ACCOUNT, TOKEN)
        message = client.messages \
            .create(
            body=f"Low Price Alert. Only ${flight.price} to fly from {flight.origin_city} - {flight.origin_airport} to {flight.destination_city} - {flight.destination_airport}, from {flight.out_date} to {flight.return_date}",
            from_='+19897621014',
            to=NUMBER
        )
        print(message.sid)