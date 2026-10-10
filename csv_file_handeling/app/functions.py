import csv
import os

def get_file_name():
    file_name = input('File name: ')
    return file_name

def create_csv_file():
    file_name = get_file_name()
    new_file = open(f"data\\{file_name}.csv", 'w')
    new_file.close()
    print('New file created.')

def edit_csv_file():
    file_name = get_file_name()
    with open(f"data\\{file_name}.csv", 'a') as editor:
        editor_file = csv.writer(editor, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        rows = 0
        try:
            rows = int(input('how many rows of data you want to add to this file? '))
            if rows <= 0:
                raise ValueError
        except:
            print('Error, please try again')
        
        for i in range(rows):
            first_name = input(f'row {i + 1} first_name: ')
            last_name = input(f'row {i + 1} last_name: ')
            age = input(f'row {i + 1} age: ')
            email = input(f'row {i + 1} email: ')
            editor_file.writerow([first_name, last_name, age, email])

        print('\nchanges saved')


def delete_csv_file():
    file_name = get_file_name()
    try:
        os.remove(f'data\\{file_name}.csv')
        print(f'{file_name}.csv was deleted.')
    except:
        print('\nfile does not exist')

def read_csv_file():
    file_name = get_file_name()
    data_list = []

    try:
        with open(f"data\\{file_name}.csv", 'r') as reader:
            info = csv.DictReader(reader)

            for row in info:
                data_list.append(row)

        for data in data_list:
            print(data)

    except FileNotFoundError:
        print('\nFile does not exist')