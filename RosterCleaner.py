import csv
import re

with open('./Class-specific files/class_roster_dirty.csv') as roster_file:
    roster = csv.reader(roster_file)
    roster.__next__()
    scholars = []
    for scholar in roster:
        lastname = scholar[0].strip()
        first = scholar[1]
        firstname = first.split(sep='(')[0].strip()
        preferredname = re.search(r'\((\w*)\)', first)
        if preferredname:
            preferredname = preferredname.group(1).strip()
        scholars.append((lastname, firstname, preferredname))


with open('./Class-specific files/class_roster_clean.csv', mode='w') as roster_clean_file:

    roster_writer = csv.writer(roster_clean_file, delimiter=',')
    fieldnames = ['Lastname', 'Firstname', 'Preferredname']
    roster_writer.writerow(fieldnames)

    for scholar in scholars:
        roster_writer.writerow(scholar)
