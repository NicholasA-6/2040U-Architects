import csv

def parse_csv(filename):
    data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

filename = 'MOCK_DATA.csv'
dict = parse_csv(filename)
print(dict)