import csv


def get_number_list():
    with open('Test Numbers - Sheet1.csv', mode='r') as file:
        csvFile = csv.reader(file)
        l = []
        for lines in csvFile:
            l.extend(lines)
        return l[:500]
