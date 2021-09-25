import csv
from enum import Enum
import os
import re

welcome_string = "Custom attendance script by Martin Diges (2021)"
welcome_string_border = '~'*len(welcome_string)
print(welcome_string_border)
print(welcome_string)
print(welcome_string_border)


class Fields(Enum):
    lastname = 'Lastname'
    firstname = 'Firstname'
    preferredname = 'Preferredname'


with open('./Class-specific files/class_roster_clean.csv') as roster_file:
    roster_csv = csv.reader(roster_file)
    roster_csv.__next__()
    # Place all scholar last names in a dict as keys. Values are arrays with an array of first/preferred names and a boolean Present value
    roster = dict()

    names_final = []
    name_index = 0
    for scholar in roster_csv:
        lastname = scholar[0].strip()
        firstname = scholar[1].strip()
        preferredname = scholar[2].strip()
        # Before we modify names, which makes them less readable, we place them in an array to be used at the end
        names_final.append((lastname, firstname))

        lastname = lastname.lower()
        firstname = firstname.lower()
        preferredname = preferredname.lower()

        if not lastname in roster:
            roster[lastname] = []
        roster[lastname].append(
            [[firstname, preferredname], False, name_index])
        name_index += 1

    # TODO make one int object shared by two different dicts so that a scholar can be searched by last, first, or preferred name

    # DEBUG
    # for scholar in roster:
    #     print('{0}:\t\t{1}'.format(scholar, roster[scholar]))

    # STEP 1, tell the program which .csv file you are wanting to examine

print('Choose an attendance file (.csv) by typing the corresponding number and hitting ENTER')

files = os.listdir('./Class-specific files')
files_valid = []
menu_counter = 0

for file in files:
    if re.search(r'.*\.csv$', file):
        if file[0:8] == '(OUTPUT)':
            continue
        print('[{0}] {1}'.format(menu_counter, file))
        files_valid.append(file)
        menu_counter += 1
print()

chosen_file = int(input())
chosen_file = files_valid[chosen_file]

# STEP 2, tell the program how the file is formatted so that it can be correctly interpreted

print('Choose the naming scheme in the file by typing the corresponding number and hitting ENTER')

attendance_formats = [
    '{0}, {1}, (Optional) {2}'.format(Fields.lastname.value,
                                      Fields.firstname.value, Fields.preferredname.value),
    '{0} {1}'.format(Fields.firstname.value, Fields.lastname.value),
    '{0}, {1}'.format(Fields.firstname.value,
                      Fields.lastname.value)]
for i, format in enumerate(attendance_formats):
    print('[{0}] {1}'.format(i, format))
print()

chosen_format = int(input())

# STEP 3, cross-reference attendance and roster files
# ALL COMPARISONS MUST IGNORE UPPER/LOWER CASE

with open('./Class-specific files/{0}'.format(chosen_file)) as attendance_file:
    attendance_reader = csv.reader(attendance_file)

    if chosen_format == 0:  # Attendance: lastname, firstname
        for scholar_attendance in attendance_reader:
            scholar_attendance = scholar_attendance[1:2]
            # DEBUG
            # print('Attendance observation: ', scholar_attendance)
            lastname = scholar_attendance[1]
            if lastname in roster:
                scholars_roster = roster[lastname]
                # There could be more than one person with the same last name
                for scholar_roster in scholars_roster:
                    # DEBUG
                    #print('Roster observation: ', scholar_roster)
                    if scholar_attendance[1] == scholar_roster[0][0] or scholar_attendance[2] == scholar_roster[0][1]:
                        # Match!
                        scholar_roster[1] = True
                        # We only match the first
                        break

    if chosen_format == 2:  # Attendance: firstname, lastname
        for scholar_attendance in attendance_reader:
            scholar_attendance = scholar_attendance[1:3]
            for i in range(len(scholar_attendance)):
                scholar_attendance[i] = scholar_attendance[i].strip().lower()
            # DEBUG
            #print('Attendance observation: ', scholar_attendance)
            lastname = scholar_attendance[1]
            if lastname in roster:
                scholars_roster = roster[lastname]
                # There could be more than one person with the same last name
                for scholar_roster in scholars_roster:
                    # DEBUG
                    #print('Roster observation: ', scholar_roster)
                    #print(scholar_attendance[0], scholar_roster[0][0], scholar_attendance[0], scholar_roster[0][1])
                    if scholar_attendance[0] == scholar_roster[0][0] or scholar_attendance[0] == scholar_roster[0][1]:
                        # DEBUG
                        # print('Match!')
                        # Match!
                        scholar_roster[1] = True
                        # We only match the first
                        break

# STEP 4, separate scholars into those who attended and those who did not

present = []
absent = []
for lastname in roster:
    for scholar in roster[lastname]:
        # DEBUG
        # print(scholar)
        if scholar[1]:
            present.append(names_final[scholar[2]])
        else:
            absent.append(names_final[scholar[2]])

# STEP 5, order lists, print out lists, and save to a file

present.sort()
absent.sort()

print("\n{0} students were present:".format(len(present)))
for scholar in present:
    print('{0}, {1}'.format(scholar[0], scholar[1]))

print("\n{0} students were not detected as present by the program:".format(len(absent)))
print("PLEASE DOUBLE-CHECK BEFORE REPORTING A SCHOLAR AS ABSENT - THEY MAY HAVE MISSPELLED THEIR NAME")
for scholar in absent:
    print('{0}, {1}'.format(scholar[0], scholar[1]))
print("PLEASE DOUBLE-CHECK BEFORE REPORTING A SCHOLAR AS ABSENT - THEY MAY HAVE MISSPELLED THEIR NAME")

print('Results will be printed to the (OUTPUT) text file')

with open('./Class-specific files/(OUTPUT) {0}'.format(chosen_file), mode='w') as output_file:
    output_file.write("{0} students were present:\n".format(len(present)))
    for scholar in present:
        output_file.write('{0}, {1}\n'.format(scholar[0], scholar[1]))
    output_file.write('\n')

    output_file.write("{0} students were absent:\n".format(len(absent)))
    output_file.write(
        'PLEASE DOUBLE-CHECK BEFORE REPORTING A SCHOLAR AS ABSENT - THEY MAY HAVE MISSPELLED THEIR NAME\n')
    for scholar in absent:
        output_file.write('{0}, {1}\n'.format(scholar[0], scholar[1]))
    output_file.write(
        'PLEASE DOUBLE-CHECK BEFORE REPORTING A SCHOLAR AS ABSENT - THEY MAY HAVE MISSPELLED THEIR NAME\n')
    output_file.write('\n')
