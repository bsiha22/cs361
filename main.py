import json
import time
import zmq

class ListOrganizer:
    def __init__(self):
        self.lists = {}
        self.filename = "listdata.json"
        self.load_lists()

    def create_list(self, list_name):
        if list_name not in self.lists:
            self.lists[list_name] = []
            self.save_lists()
            print(f"List '{list_name}' created.")
            time.sleep(1)

    def add_item(self, list_name):
        if list_name in self.lists:
            added_items = []
            while True:
                confirmation = input("Enter 'cancel' to cancel adding items.\n"
                                     "Enter 'confirm' to finish adding items,\n"
                                     "Or enter the name of the item to continue adding: ")
                if confirmation.lower() == "cancel":
                    print("Item addition canceled.")
                    time.sleep(1)
                    return  # Cancel the operation
                elif confirmation.lower() == "confirm":
                    self.lists[list_name].extend(added_items)
                    self.save_lists()
                    print("Items added successfully.")
                    time.sleep(1)
                    break
                else:
                    item_price = float(input("Enter the price of the item: "))
                    item_location = input("Enter the location of the item (optional, enter 'N/A' or leave blank if not applicable): ")
                    item_restrictions = input("Enter the restrictions of the item (optional, enter 'N/A' or leave blank if not applicable): ")
                    item = Item(confirmation, item_price, item_location, item_restrictions)
                    added_items.append(item.__dict__)
        else:
            print(f"List '{list_name}' not found.")
            time.sleep(1)

    def remove_item(self, list_name):
        if list_name in self.lists:
            itemname = input("Enter the name of the item to be removed: ")
            for item in self.lists[list_name]:
                if item["name"].lower() == itemname.lower():
                    self.lists[list_name].remove(item)
                    print(f"{itemname} was deleted from {list_name}.")
                    self.save_lists()
                    time.sleep(1.5)
                    return
            print(f"{itemname} was not found in the list '{list_name}'.")
        else:
            print(f"List '{list_name}' not found.")
            time.sleep(1)

    def rename_item(self, list_name):
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5555")
            oldname = input("Enter the old name to be changed: ")
            newname = input("Enter the new name: ")
            socket.send_string(f'rename,{list_name},{oldname},{newname}')
            response = socket.recv_string()
            print(response)

    def search_items(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:3333")

        item = input("Enter the name of the item you want to search: ")
        socket.send_string(item)
        response = socket.recv_string()
        print()
        print(response)
        print()
        input("Enter anything to continue: ")

    def recommend(self):
        rec = input("Enter 1 for fruit,\n"
                    "2 for vegetables,\n"
                    "3 for sweets,\n"
                    "4 for household items,\n"
                    "or 5 for smoothie ingredients.\n"
                    "Enter anything else to return: ")
        if rec in ("1", "2", "3", "4", "5"):
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:4444")
            socket.send_string(rec)
            response = socket.recv_string()
            print()
            print(response)
            print()
            input("Enter anything to continue: ")
        else:
            print("Returning...")
            time.sleep(1)

    def sort_list(self, list_name, key):
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:6666")
            socket.send_string(f'{key},{list_name}')
            response = socket.recv_string()
            print(response)


    def rename_list(self, old_name):
        if old_name in self.lists:
            newname = input("Enter a new name for this list: ")
            confirm = input("Enter 'confirm' to rename or 'cancel' to return to the home page: ")
            if confirm == 'cancel':
                return
            elif confirm == 'confirm':
                self.lists[newname] = self.lists.pop(old_name)
                self.save_lists()
                print(f"List '{old_name}' renamed to '{newname}' successfully.")
                time.sleep(1)
        else:
            print(f"List '{old_name}' not found.")
            time.sleep(1)
    
    def delete_list(self, listname):
        if listname in self.lists:
            print("Warning: Deleting a list also deletes all of its items, which cannot be recovered.")
            time.sleep(1)
            confirm = input("Enter 'confirm' to delete or 'cancel' to return to the home page: ")
            if confirm == 'cancel':
                return
            elif confirm == 'confirm':
                del self.lists[listname]
                self.save_lists()
                print(f"List '{listname}' has been deleted successfully.")
                time.sleep(1)
        else:
            print(f"List '{listname}' not found.")
            time.sleep(1)

    def display_list(self, list_name):
        if list_name in self.lists:
            if self.lists[list_name] == []:
                print(f"\n{list_name} is empty!")
            else:
                print(f"List '{list_name}':")
                for item in self.lists[list_name]:
                    print("-", Item(**item))
                
                time.sleep(1)
                next = input("\nEnter 1 to add an item to this list,\n" 
                             "2 to delete an item from this list, \n"
                      "3 to rename an item in this list, \n" 
                      "4 to sort this list by name, \n"
                      "5 to sort this list by price,\n"
                      "or anything else to return to the home page: ")
                if next == "1":
                    self.add_item(list_name)
                elif next == "2":
                    self.remove_item(list_name)
                elif next == "3":
                    self.rename_item(list_name)
                elif next == "4":
                    self.sort_list(list_name, 'name')
                elif next == "5":
                    self.sort_list(list_name, 'price')
        else:
            print(f"List '{list_name}' not found.")
            time.sleep(1)

    def display_lists(self):
        if self.lists:
            print("")
            print("Available lists:")
            for list_name in self.lists:
                print("-", list_name)

            time.sleep(1)

            listname = input("\nEnter the name of a list to view its contents, \n"
                             "or enter anything else to return to the home page: ")
            if listname in self.lists:
                self.display_list(listname)
            time.sleep(1)
        else:
            print("No lists available.")
            time.sleep(1)

    def save_lists(self):
        with open(self.filename, "w") as data:
            json.dump(self.lists, data, indent=4, ensure_ascii=False)

    def load_lists(self):
        with open(self.filename, "r") as data:
            self.lists = json.load(data)
    
    def test_lists(self):
        for item in self.lists:
            print(item)

    def tutorial(self):
        print("This app's main feature is creation and management of lists.")
        time.sleep(2)
        print("There are 4 features that come with this: Creating lists, adding items to lists,")
        time.sleep(2)
        print("deleting lists and items, and renaming lists.")
        time.sleep(2)
        print("Creating lists can be done by entering 1 on the home page.")
        time.sleep(2)
        print("Adding items can be done in Option 2, but can also be accessed when viewing lists through Options 6 and 7.")
        time.sleep(2)
        print("Deleting items can be done in Option 3, and can be similarly accessed in Options 6 and 7.")
        time.sleep(2)
        print("Deleting a list can be done in Option 5, and renaming a list is done in Option 4.")
        time.sleep(2)
        input("Enter anything to return to the home page: ")

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
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    print("Welcome to List Organizer")
    time.sleep(1)
    print("This program allows you to create shopping lists that help you stay organized.")
    time.sleep(1)
    print("List names are case-sensitive.")
    time.sleep(1)

    while True:
        print("\nEnter a number to select an option:")
        time.sleep(1)
        print("\n1. Create a new list")
        print("2. Add items to a list")
        print("3. Delete an item from a list")
        print("4. Rename a list")
        print("5. Delete a list")
        print("6. View a list's contents")
        print("7. View all lists")
        print("8. Search lists by item name")
        print("9. Get Grocery Recommendations")
        print("0. Tutorial")
        print("Enter anything else to exit.")
        organizer.load_lists()

        choice = input("Enter your choice: ")

        if choice == "1":
            list_name = input("Enter the name of the new list: ")
            organizer.create_list(list_name)
        elif choice == "2":
            list_name = input("Enter the name of the list to add to: ")
            organizer.add_item(list_name)
        elif choice == "3":
            list_name = input("Enter the name of the list to delete from: ")
            organizer.remove_item(list_name)
        elif choice == "4":
            list_name = input("Enter the name of the list you want to rename, \n"
                              "to cancel this, enter 'cancel': ")
            if list_name.lower() != 'cancel':
                organizer.rename_list(list_name)
        elif choice == "5":
            list_name = input("Enter the name of the list to be deleted, \n"
                              "to cancel this, enter 'cancel': ")
            if list_name.lower() != 'cancel':
                organizer.delete_list(list_name)
        elif choice == "6":
            list_name = input("Enter the name of the list: ")
            organizer.display_list(list_name)
        elif choice == "7":
            organizer.display_lists()
        elif choice == "8":
            organizer.search_items()
        elif choice == "9":
            organizer.recommend()
        elif choice == "0":
            organizer.tutorial()
        else:
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()
