# You need PyTest for this
import random
import back_end

def setup_module():
    data = ""
    with open("MOCK_DATA.csv", "r+") as file:
        data = file.read()
    with open("TEST_DATA.csv", "w+") as file:
        file.write(data)

def test_get_user():
    val1 = str(random.randint(0, 9999))
    val2 = str(random.randint(0, 9999))
    val3 = str(random.randint(0, 9999))
    with open("TEST_DATA.csv", "a") as file:
        file.write(f"{val1},{val2},{val3}")
    assert back_end.get_user(val1, "TEST_DATA.csv")[0] == [val1, val2, val3]

def test_add_to_file():
    val1 = random.randint(0, 9999)
    val2 = random.randint(0, 9999)
    val3 = random.randint(0, 9999)
    back_end.add_to_file(val1, val2, val3, "TEST_DATA.csv")
    last_line = ""
    with open("TEST_DATA.csv", "r") as file:
        for line in file:
            last_line = line.strip()
    assert last_line == f"{val1},{val2},{val3}"

def test_replace_user():
    val1 = str(random.randint(0, 9999))
    val2 = str(random.randint(0, 9999))
    val3 = str(random.randint(0, 9999))
    val4 = str(random.randint(0, 9999))
    val5 = str(random.randint(0, 9999))
    print(val1, val2, val3, val4, val5)
    with open("TEST_DATA.csv", "a") as file:
        file.write(f"{val1},{val2},{val3}")
    back_end.replace_user([val1, val2, val3], [val1, val4, val5])
    last_line = ""
    with open("TEST_DATA.csv", "r") as file:
        for line in file:
            last_line = line.strip()
    assert last_line == f"{val1},{val4},{val5}"
