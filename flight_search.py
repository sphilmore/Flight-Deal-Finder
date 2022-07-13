import os

import requests
from datetime import datetime, timedelta

from flight_data import FlightData

FLIGHT_SEARCH_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
FLIGHT_API_KEY = os.getenv("API_KEY")
today = datetime.now()
tomorrow_date = (today + timedelta(days=1))
six_months_date = (tomorrow_date + timedelta(days=183))

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
     def get_destination_code(self, city_name):
            headers = {
                "apikey": FLIGHT_API_KEY
            }
            query ={
                "term": city_name,
                "location_types": "city",
            }
            response = requests.get(url=FLIGHT_SEARCH_ENDPOINT, headers=headers, params=query)
            results = response.json()["locations"]
            code = results[0]["code"]
            return code


     def flight_info(self, origin_city_code, destination_city_code,):
        headers = {
             "apikey": FLIGHT_API_KEY
         }
        parameters = {

            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": tomorrow_date.strftime("%d/%m/%Y"),
            "date_to": six_months_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(url="https://tequila-api.kiwi.com/v2/search", params=parameters, headers=headers)
        print(response.json())
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data