import csv

filename = 'MOCK_DATA.csv'

def parse_csv(filename):
    data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def get_user(username):
    data = parse_csv(filename)
    for i in data:
        if i[0] == username:
            return i
    return None

def get_names():
    data = parse_csv(filename)
    newdata = []
    for i in data:
        newdata.append(i[0])
    return newdata
