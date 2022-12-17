from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep


class GoogleBot:
    def __init__(self):
        self.my_service = Service("C:/Zoo_Development/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.my_service)
        self.google_form = "https://forms.gle/G2MwQkpo3pbV227N8"

    def start_filling(self):
        self.driver.get(self.google_form)
        sleep(5)

    def fill_form(self, list_value):
        input_bars = self.driver.find_elements(By.CSS_SELECTOR, ".Xb9hP input")
        for position in range(len(input_bars)):
            input_bars[position].click()
            sleep(1)
            input_bars[position].send_keys(f"{list_value[position + 1]}")
            sleep(3)

    def send_form(self):
        send_button = self.driver.find_element(By.CSS_SELECTOR, ".lRwqcd div span")
        send_button.click()
        sleep(5)

    def fill_again(self):
        again_button = self.driver.find_element(By.CSS_SELECTOR, ".c2gzEf a")
        again_button.click()
        sleep(5)
