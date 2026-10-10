from app import functions
import sys

def exit_program():
    sys.exit()

def checking_options(option: int):
    try:
        if option == 1:
            functions.create_csv_file()
        elif option == 2:
            functions.edit_csv_file()
        elif option == 3:
            functions.delete_csv_file()
        elif option == 4:
            functions.read_csv_file()
        else:
            exit_program()
    except:
        exit_program()

option = int(input(
    'Welcome\n' \
    'Choose an option:\n' \
    '1. Create a CSV file\n' \
    '2. Edit a CSV file\n' \
    '3. Delete a CSV file\n'\
    '4. Read a CSV file\n'
))

checking_options (option)


