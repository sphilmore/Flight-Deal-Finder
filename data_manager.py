import requests
SHETTY_END_POINT = "https://api.sheety.co/639bea7e163a1c98657b6a6331b79d6c/takeMeThere/sheet1"


class DataManager:
    def __init__(self):
        self.destination ={}
    #This class is responsible for talking to the Google Sheet.
    def get_destination_data(self):
        response = requests.get(url=SHETTY_END_POINT)
        data = response.json()['sheet1']
        self.destination = data
        return self.destination
    def update_code(self):
        for city in self.destination:
            parameters = {
                 "sheet1": {
                     "iataCode": city["iataCode"]
                }
            }
            put_response = requests.put(url=f"{SHETTY_END_POINT}/{city['id']}", json=parameters)

            print(put_response.text)



