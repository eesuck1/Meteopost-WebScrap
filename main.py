import scrapper
import dataset


def main():
    scr = scrapper.Scrapper()
    scr.scrap()

    dictionary = scr.get_data()

    data = dataset.Dataset(dictionary)

    data.create_csv(data.create_path("Data", "comma"))


if __name__ == '__main__':
    main()
