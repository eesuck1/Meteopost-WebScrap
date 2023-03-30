import scrapper
import dataset


def main():
    scr = scrapper.Scrapper()
    scr.scrap()
    #
    # dictionary = scr.get_data()
    #
    # data = dataset.Dataset(dictionary)
    #
    # data.create_excel(data.create_path("Data", "sheet"))


if __name__ == '__main__':
    main()
