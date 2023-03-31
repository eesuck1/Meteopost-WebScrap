import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
import bs4

import constants
import dataset


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
        self.__frame__ = None

    @staticmethod
    def __start_info__() -> None:
        print(f"[INFO] Work is started.")

    @staticmethod
    def __done_info__() -> None:
        print(f"[INFO] Work is done.")

    def __create_dictionary__(self) -> None:
        self.__dictionary__ = {category: [] for category in constants.CATEGORIES}

    def scrap(self, result_folder: str) -> None:
        self.__start_info__()

        self.__options__ = Options()
        self.__options__.headless = True

        self.__browser__ = webdriver.Edge(options=self.__options__)
        self.__browser__.get(constants.URL)

        self.__full_parse__(result_folder)

        self.__done_info__()

    def __full_parse__(self, result_folder: str) -> None:
        self.years = Select(self.__browser__.find_element(By.XPATH, constants.YEAR_XPATH))

        for year_index in range(len(os.listdir(result_folder)), len(self.years.options)):
            self.__create_dictionary__()

            self.years = Select(self.__browser__.find_element(By.XPATH, constants.YEAR_XPATH))
            self.years.select_by_index(year_index)

            self.__update__()

            self.__frame__ = dataset.Dataset(self.get_data())
            self.__frame__.create_csv(self.__frame__.create_path(result_folder, f"{2010 + year_index}"))

    def __update__(self) -> None:
        self.cities = Select(self.__browser__.find_element(By.XPATH, constants.SELECT_XPATH))

        for city_index in range(len(self.cities.options)):
            try:
                self.cities = Select(self.__browser__.find_element(By.XPATH, constants.SELECT_XPATH))
                city = self.cities.options[city_index].text

                self.cities.select_by_index(city_index)

                button = self.__browser__.find_element(By.XPATH, constants.BUTTON_XPATH)
                button.click()

                self.__parse__(self.__browser__.page_source, city)
            except WebDriverException:
                continue

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
