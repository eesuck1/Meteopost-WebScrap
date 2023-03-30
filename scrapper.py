import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import bs4

import constants


class Scrapper:
    __instance__ = None

    def __init__(self):
        self.browser = None
        self.options = None
        self.soup = None

    def __new__(cls, *args, **kwargs):
        if Scrapper.__instance__ is None:
            Scrapper.__instance__ = super().__new__(cls)

            Scrapper.__start_info__()
            Scrapper.scrap(Scrapper.__instance__)
            Scrapper.__done_info__()

        return Scrapper.__instance__

    @staticmethod
    def __start_info__():
        print(f"[INFO] Work is started.")

    @staticmethod
    def __done_info__():
        print(f"[INFO] Work is done.")

    def scrap(self):
        self.options = Options()
        self.options.headless = True

        self.browser = webdriver.Edge(options=self.options)
        self.browser.get(constants.URL)

        self.__update__()
        self.__parse__(self.browser.page_source)

    def __update__(self):
        selected_element = self.browser.find_element(By.XPATH, constants.SELECT_XPATH)
        selected_element.click()

        selected_element.find_element(By.XPATH, constants.LVIV_FIELD_XPATH).click()

        button = self.browser.find_element(By.XPATH, constants.BUTTON_XPATH)
        button.click()

    def __parse__(self, page_source: str):
        self.soup = bs4.BeautifulSoup(page_source, "html.parser")

        columns = self.soup.find_all("td", text=re.compile(r'-|\d+'))
        for column in columns:
            print(column.text)