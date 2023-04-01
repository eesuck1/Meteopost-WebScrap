import os

import pandas


class Dataset:
    def __init__(self, dictionary=None):
        if dictionary is None:
            dictionary = {}

        self.__data_frame__ = pandas.DataFrame(self.__check_dictionary__(dictionary))
        self.__formats_dictionary__ = {
            ".csv": pandas.read_csv,
            ".xlsx": pandas.read_excel,
        }

    @staticmethod
    def __check_dictionary__(dictionary: dict) -> dict:
        lengths = [len(value) for value in dictionary.values()]

        for key in dictionary:
            dictionary[key] = dictionary[key][:min(lengths)]

        return dictionary

    @staticmethod
    def create_path(folder_name: str, file_name: str) -> str:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        return os.path.join(folder_name, file_name)

    def create_csv(self, path: str) -> None:
        self.__data_frame__.to_csv(path + ".csv", index=False)

    def create_excel(self, path: str) -> None:
        self.__data_frame__.to_excel(path + ".xlsx", index=False)

    def get_data_frame(self) -> pandas.DataFrame:
        return self.__data_frame__

    def concatenate_frame(self, folder: str, file_format: str, result_name: str, to_save: bool) -> pandas.DataFrame:
        concatenated_frame = pandas.DataFrame()

        for file in os.listdir(folder):
            if file.endswith(file_format):
                temporary = self.__formats_dictionary__[file_format](self.create_path(folder, file))

                concatenated_frame = pandas.concat([concatenated_frame, temporary], ignore_index=True)
        if to_save:
            concatenated_frame.to_csv(self.create_path(folder, result_name + file_format), index=False)

        return concatenated_frame

