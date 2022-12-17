import requests
from bs4 import BeautifulSoup
from Zillow_File import ZillowInfo


class RentInformation:
    def __init__(self):
        hand = ZillowInfo()
        self.address = hand.website_url
        self.my_header = {
            "Accept-Language": hand.my_language,
            "User-Agent": hand.my_agent
        }

    def get_rent_info(self):
        respond = requests.get(url=self.address, headers=self.my_header)
        website = respond.text
        soup = BeautifulSoup(website, "html.parser")
        # -------------- find home addresses -------------- #
        homes = soup.select(selector="li article div div a address")
        home_address = [item.getText() for item in homes]
        #  -------------- find home prices -------------- #
        prices = soup.select(selector="li article div div div:nth-of-type(2) span")
        home_prices = [item.getText()[:6] for item in prices if len(item.getText()) > 2]
        #  -------------- find home links -------------- #
        links = soup.select(selector="li article div div a")
        home_links = [f"https://www.zillow.com/{item.get('href')}" for item in links]
        for dub_link in home_links:
            if dub_link.count("www.zillow.com") > 0:
                home_links.remove(dub_link)
        #  -------------- received result -------------- #
        answer = {
            "address": home_address,
            "prices": home_prices,
            "links": home_links
        }
        return answer
