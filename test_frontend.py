from app import *

testdata_filepath = os.path.join(os.path.dirname(__file__), "data", "testdata.csv")


def test_load_watches_from_csv():
    load_watches_from_csv(testdata_filepath)
    with open(testdata_filepath, newline="") as file:
        for line in file:
            data = line.split(",")
            for entry in catalogue.watches:
                if data[0] == entry.name:
                    pass
