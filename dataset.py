import os

import pandas


class Dataset:
    def __init__(self, dictionary: dict):
        self.__data_frame__ = pandas.DataFrame(dictionary)

    @staticmethod
    def create_path(folder_name: str, file_name: str) -> str:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        return os.path.join(folder_name, file_name)

    def create_csv(self, path: str) -> None:
        self.__data_frame__.to_csv(path + ".csv", index=False)

    def create_excel(self, path: str) -> None:
        self.__data_frame__.to_excel(path + ".xlsx", index=False)