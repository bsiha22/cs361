import json
import time

class ListOrganizer:
    def __init__(self):
        self.lists = {}
        self.filename = "listdata.json"
        self.load_lists()

    def create_list(self, list_name):
        if list_name not in self.lists:
            self.lists[list_name] = []
            self.save_lists()

    def add_item(self, list_name):
        if list_name in self.lists:
            added_items = []
            while True:
                confirmation = input("Enter 'cancel' to cancel adding items.\n"
                                     "Enter 'done' to finish adding items,\n"
                                     "Or enter the name of the item to add: ")
                if confirmation.lower() == "cancel":
                    print("Item addition canceled.")
                    return  # Cancel the operation
                elif confirmation.lower() == "done":
                    self.lists[list_name].extend(added_items)
                    self.save_lists()
                    print("Item added successfully.")
                    break
                else:
                    item_price = float(input("Enter the price of the item: "))
                    item_location = input("Enter the location of the item (optional, enter 'N/A' or leave blank if not applicable): ")
                    item_restrictions = input("Enter the restrictions of the item (optional, enter 'N/A' or leave blank if not applicable): ")
                    item = Item(confirmation, item_price, item_location, item_restrictions)
                    added_items.append(item.__dict__)
        else:
            print(f"List '{list_name}' not found.")

    def remove_item(self, list_name):
        if list_name in self.lists:
            itemname = input("Enter the name of the item to be removed:")
            for item in self.lists[list_name]:
                if item["name"].lower() == itemname.lower():
                    self.lists[list_name].remove(item)
                    self.save_lists()
                    return
            print(f"{itemname} was not found in the list '{list_name}'.")
        else:
            print(f"List '{list_name}' not found.")

    def rename_list(self, old_name):
        if old_name in self.lists:
            newname = input("Enter a new name for this list:")
            confirm = input("Enter 'confirm' to rename or 'cancel' to return to the home page: ")
            if confirm == 'cancel':
                return
            elif confirm == 'confirm':
                self.lists[newname] = self.lists.pop(old_name)
                self.save_lists()
                print(f"List '{old_name}' renamed to '{newname}' successfully.")
        else:
            print(f"List '{old_name}' not found.")
    
    def delete_list(self, listname):
        if listname in self.lists:
            confirm = input("Enter 'confirm' to delete or 'cancel' to return to the home page: ")
            if confirm == 'cancel':
                return
            elif confirm == 'confirm':
                del self.lists[listname]
                self.save_lists()
                print(f"List '{listname}' has been deleted successfully.")
        else:
            print(f"List '{listname}' not found.")

    def display_list(self, list_name):
        if list_name in self.lists:
            if self.lists[list_name] == []:
                print(f"\n{list_name} is empty!")
            else:
                print(f"List '{list_name}':")
                for item in self.lists[list_name]:
                    print("-", Item(**item))
        else:
            print(f"List '{list_name}' not found.")

    def display_lists(self):
        if self.lists:
            print("")
            print("Available lists:")
            for list_name in self.lists:
                print("-", list_name)
        else:
            print("No lists available.")

    def save_lists(self):
        with open(self.filename, "w") as data:
            json.dump(self.lists, data, indent=4, ensure_ascii=False)

    def load_lists(self):
        with open(self.filename, "r") as data:
            self.lists = json.load(data)
    
    def test_lists(self):
        for item in self.lists:
            print(item)

class Item:
    def __init__(self, name, price, store=None, limits=None):
        self.price = price
        self.name = name
        self.store = store if store else "N/A"
        self.limits = limits if limits else "N/A"

    def __str__(self):
        return f"{self.name} - Price: {self.price}, Store: {self.store}, Restrictions: {self.limits} "


def main():
    organizer = ListOrganizer()
    print("Welcome to List Organizer")
    time.sleep(1)
    print("This program allows you to create shopping lists that help you stay organized.")
    time.sleep(1)

    while True:
        print("\nEnter a number to select an option:")
        time.sleep(1)
        print("\n1. Create a new list")
        print("2. Add items to a list")
        print("3. Remove an item from a list")
        print("4. Rename a list")
        print("5. Delete a list")
        print("6. View a list's contents")
        print("7. View all lists")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_name = input("Enter the name of the list: ")
            organizer.create_list(list_name)
        elif choice == "2":
            list_name = input("Enter the name of the list: ")
            organizer.add_item(list_name)
        elif choice == "3":
            list_name = input("Enter the name of the list: ")
            organizer.remove_item(list_name)
        elif choice == "4":
            list_name = input("Enter the name of the list you want to rename:")
            organizer.rename_list(list_name)
        elif choice == "5":
            list_name = input("Enter the name of the list to be deleted:")
            organizer.delete_list(list_name)
        elif choice == "6":
            list_name = input("Enter the name of the list: ")
            organizer.display_list(list_name)
        elif choice == "7":
            organizer.display_lists()
        elif choice == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
