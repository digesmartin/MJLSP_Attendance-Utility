import csv

with open('class_roster.csv') as roster_file:
    roster = csv.reader(roster_file)

    for row in roster:
        print(row)