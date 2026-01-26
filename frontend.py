# imports
import csv
import os

# get back_end functions
from back_end import parse_csv, get_user


# instantiate items
items = []

# display menu function
def display_menu():
    print("-"*25)
    print("MAIN MENU")
    print("-"*25)
    print("1. View All Items\n2. Load Next 10 Items\n3.View Item\n0. Exit")
    print("-"*25)

# get the backend function
def load_data():
    global items
    items = parse_csv("MOCK_DATA.csv")
    print(f"loaded {len(items)} items")

def display_items():
    if not items:
        print("no items")
        return
    for item in items:
        print(item)

# load the data
load_data()

# main loop
while True:
    display_menu()
    choice = input("\nEnter your choice: ").strip()
    if (choice == "1"):
        display_items()
        input("Press ENTER to return back to menu")
    elif (choice == "2"):
        # display_next_ten_items()
        input("Press ENTER to return back to menu\nOR\npress N, then ENTER to read next 10 items\n")
    elif (choice == "3"):
        get_user()
        input("Press ENTER to return back to menu")
    elif (choice == "0"):
        # view_item()
        input("Bye!")
        break
    else:
        print("Invalid choice!")