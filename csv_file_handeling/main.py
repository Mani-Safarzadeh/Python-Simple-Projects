from app import create, read
import sys

def exit_program():
    sys.exit()

def checking_options(option: int):
    try:
        if option == 1:
            create.File.create()
        elif option == 2:
            read.File.read()
        else:
            exit_program()
    except:
        exit_program()



print("Welcome")
print("Choose an option:")
print('1. Create a CSV file')
print('2. Open a CSV file')
print('3. exit')

option = int(input())

checking_options (option)

