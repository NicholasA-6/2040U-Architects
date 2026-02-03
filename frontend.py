# imports
import csv
import os

# get back_end functions
from back_end import get_user, add_to_file, replace_user


# instantiate items
items = []

def input_int(message):
    while True:
        val = input(message)
        try:
            intval = int(val)
            return intval
        except ValueError as error:
            print(error)
            print("Please enter an integer")


# display menu function
def display_menu():
    print("-"*25)
    print("MAIN MENU")
    print("-"*25)
    print("1. View All Items\n2. View Item\n3. Add Item\n4. Edit Existing Item\n0. Exit")
    print("-"*25)

def display_items():
    if not items:
        print("no items")
        return
    for item in items:
        print(item)

# main loop
while True:
    display_menu()
    choice = input("\nEnter your choice: ").strip()
    if choice == "1":
        display_items()
        input("Press ENTER to return back to menu")
    elif choice == "2":
        name = input("Please enter username to view: ")
        data = get_user(name)
        print(f"{len(data)} entries with username \"{name}\" found")
        for i in data:
            print(f"Name: {i[0]}\nAge: {i[1]}\nCountry: {i[2]}")
        input("Press ENTER to return back to menu")
    elif choice == "3":
        name = input("Please enter new username: ")
        age = input(f"Please enter age for user {name}: ")
        country = input(f"Please enter country for user {name}: ")
        add_to_file(name, age, country)
        print(f"User {name} added")
    elif choice == "4":
        username = input("Please enter username to edit: ")
        data = get_user(username)
        print(f"Found {len(data)} entries for {username}")
        if len(data) == 0:
            print("No users by that name")
        else:
            for i in data:
                print(f"[1]\nName: {i[0]}\nAge: {i[1]}\nCountry: {i[2]}")
            if len(data) >= 2:
                num = input("Please choose entry to edit: ")
                data = data[int(num) - 1]
            else:
                data = data[0]
            olddata = data.copy()
            print(f"Please enter new values for {username}. Leave empty to keep old value (old values in parentheses)")
            data[0] = input(f"Name ({data[0]}): ").strip() or data[0]
            data[1] = input(f"Age ({data[1]}): ").strip() or data[1]
            data[2] = input(f"Country  ({data[2]}): ").strip() or data[2]
            replace_user(olddata, data)
            print(f"User edited, Name: {data[0]}, Age: {data[1]}, Country: {data[2]}")
        input("Press ENTER to return back to menu")
    elif choice == "0":
        print("Bye!")
        break
    else:
        print("Invalid choice!")