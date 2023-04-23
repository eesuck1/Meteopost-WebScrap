import dataset


def main():
    frame = dataset.Dataset()

    frame.prepare_frame("Data", ".csv", "data", True, "Prepared")


if __name__ == '__main__':
    main()
