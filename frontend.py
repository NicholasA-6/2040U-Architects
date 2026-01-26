import csv
import os

def display_menu():
    print("-"*25)
    print("MAIN MENU")
    print("-"*25)
    print("1. View All Items\n2. Load Next 10 Items\n3.View Item\n0. Exit")
    print("-"*25)

while True:
    display_menu()
    choice = input("\nEnter your choice: ")
    if (choice == "1"):
        # display_all_items()
        input("Press ENTER to return back to menu")
    elif (choice == "2"):
        # display_next_ten_items()
        input("Press ENTER to return back to menu\nOR\npress N, then ENTER to read next 10 items\n")
    elif (choice == "3"):
        # view_item()
        input("Press ENTER to return back to menu")
    elif (choice == "0"):
        # view_item()
        input("Bye!")
        break
    else:
        print("Invalid choice!")