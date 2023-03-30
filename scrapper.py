import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
import bs4

import constants


class Scrapper:
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if Scrapper.__instance__ is None:
            Scrapper.__instance__ = super().__new__(cls)

        return Scrapper.__instance__

    def __init__(self):
        self.__browser__ = None
        self.__options__ = None
        self.__soup__ = None
        self.__dictionary__ = None

    @staticmethod
    def __start_info__():
        print(f"[INFO] Work is started.")

    @staticmethod
    def __done_info__():
        print(f"[INFO] Work is done.")

    def scrap(self) -> None:
        self.__start_info__()

        self.__dictionary__ = {category: [] for category in constants.CATEGORIES}
        self.__options__ = Options()
        self.__options__.headless = True

        self.__browser__ = webdriver.Edge(options=self.__options__)
        self.__browser__.get(constants.URL)

        self.__full_parse__()

        self.__done_info__()

    def __full_parse__(self) -> None:
        self.years = Select(self.__browser__.find_element(By.XPATH, constants.YEAR_XPATH))

        for i in range(len(self.years.options)):
            self.years = Select(self.__browser__.find_element(By.XPATH, constants.YEAR_XPATH))
            self.years.select_by_index(i)

            self.__update__()
            self.__parse__(self.__browser__.page_source, "Lviv")

    def __update__(self) -> None:
        selected_element = self.__browser__.find_element(By.XPATH, constants.SELECT_XPATH)
        selected_element.click()

        selected_element.find_element(By.XPATH, constants.LVIV_FIELD_XPATH).click()

        button = self.__browser__.find_element(By.XPATH, constants.BUTTON_XPATH)
        button.click()

    def __parse__(self, page_source: str, city: str) -> None:
        self.__soup__ = bs4.BeautifulSoup(page_source, "html.parser")
        columns = self.__soup__.find_all("td", text=re.compile(r'-|\d+'))

        for index, column in enumerate(columns):
            if index % len(constants.CATEGORIES[1:]) == 0:
                self.__dictionary__[constants.CATEGORIES[0]].append(city)

            self.__dictionary__[constants.CATEGORIES[1:][index % len(constants.CATEGORIES[1:])]].append(column.text)

    def get_data(self) -> dict:
        if self.__dictionary__:
            return self.__dictionary__

        return {}
