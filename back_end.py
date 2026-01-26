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
    newdata = []
    for i in data:
        if i[0] == username:
            newdata.append(i)
    return newdata

def get_names():
    data = parse_csv(filename)
    newdata = []
    for i in data:
        newdata.append(i[0])
    return newdata

def add_to_file(username, age, country):
    data = parse_csv(filename)
    newdata = [username, age, country]
    data.append(newdata)
    with open(filename, 'w', newline='') as fd:
        csvwriter = csv.writer(fd)
        csvwriter.writerows(data)