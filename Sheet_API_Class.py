import requests


class SheetApi:
    def __init__(self):
        self.my_token = "Bearer Love"
        self.my_header = {
            "Authorization": self.my_token
        }
        self.my_id = "f79e4767ff5cb4f9d47ed14cac769be5"
        self.my_project = "searchRentingHouse (responses)"
        self.my_sheet = "formResponses1"
        self.my_endpoint = f"https://api.sheety.co/{self.my_id}/{self.my_project}/{self.my_sheet}"

    def get_data(self):
        respond = requests.get(url=self.my_endpoint, headers=self.my_header)
        data = respond.json()["formResponses1"]
        time_stamps = [item["timestamp"].split()[-1] for item in data]
        locations = [item["whatIsLocation?"] for item in data]
        prices = [item["whatIsPrice?"] for item in data]
        result = {
            "times": time_stamps,
            "locations": locations,
            "prices": prices
        }
        return result
