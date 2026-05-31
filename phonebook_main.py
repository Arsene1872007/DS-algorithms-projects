import re

# ---------------- CONTACT ----------------

class Contact:
    def __init__(self, name, phone_no):
        self.name = name
        self.phone_no = phone_no
        self.next = None


# ---------------- HASH TABLE ----------------

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [None] * size

    def hash_function(self, key):
        return sum(ord(char) for char in key.lower()) % self.size

    def insert(self, name, phone_no):
        index = self.hash_function(name)

        new_contact = Contact(name, phone_no)

        if self.buckets[index] is None:
            self.buckets[index] = new_contact
            return

        current = self.buckets[index]

        while current:
            if current.name.lower() == name.lower():
                current.phone_no = phone_no
                return

            if current.next is None:
                break

            current = current.next

        current.next = new_contact

    def search(self, name):
        index = self.hash_function(name)

        current = self.buckets[index]

        while current:
            if current.name.lower() == name.lower():
                return current

            current = current.next

        return None

    def delete(self, name):
        index = self.hash_function(name)

        current = self.buckets[index]
        previous = None

        while current:
            if current.name.lower() == name.lower():

                if previous is None:
                    self.buckets[index] = current.next
                else:
                    previous.next = current.next

                return True

            previous = current
            current = current.next

        return False

    def display(self):
        print("\n----- PHONEBOOK -----")

        empty = True

        for i in range(self.size):
            current = self.buckets[i]

            while current:
                print(f"Name: {current.name} | Phone: {current.phone_no}")
                empty = False
                current = current.next

        if empty:
            print("Phonebook is empty.")

        print("---------------------")


# ---------------- VALIDATION ----------------

def validate_phone(phone_no):
    checkdigits = re.sub(r"[\s\-\+]", "", phone_no)
    return checkdigits.isdigit() and len(checkdigits) >= 10


def validate_name(name):
    return bool(name.strip()) and all(
        c.isalpha() or c in " -" for c in name
    )


# ---------------- PHONEBOOK FUNCTIONS ----------------

def add_contact(hash_table, name, phone_no):
    if not validate_name(name):
        return "Invalid name"

    if not validate_phone(phone_no):
        return "Invalid phone number"

    if hash_table.search(name):
        return f"Contact '{name}' already exists"

    hash_table.insert(name, phone_no)
    return f"Contact '{name}' added successfully"


def search_contact(hash_table, name):
    contact = hash_table.search(name)

    if not contact:
        return f"Contact '{name}' not found"

    return f"Name: {contact.name} | Phone: {contact.phone_no}"


def delete_contact(hash_table, name):
    if not hash_table.search(name):
        return f"Contact '{name}' not found"

    hash_table.delete(name)
    return f"Contact '{name}' deleted successfully"


def update_contact(hash_table, name, new_phone_no):
    if not validate_phone(new_phone_no):
        return "Invalid phone number"

    contact = hash_table.search(name)

    if not contact:
        return f"Contact '{name}' not found"

    contact.phone_no = new_phone_no
    return f"Contact '{name}' updated successfully"


# ---------------- TESTING ----------------

def run_tests(phonebook):
    print("\n===== RUNNING TESTS =====")

    print(add_contact(phonebook, "Alice", "1234567890"))
    print(add_contact(phonebook, "Bob", "9876543210"))

    print(search_contact(phonebook, "Alice"))

    print(update_contact(phonebook, "Alice", "1112223333"))
    print(search_contact(phonebook, "Alice"))    


    print(delete_contact(phonebook, "Bob"))
    print(search_contact(phonebook, "Bob"))

    print(add_contact(phonebook, "", "1234567890"))
    print(add_contact(phonebook, "John", "123"))

    print("===== TESTS FINISHED =====\n")


# ---------------- USER INTERFACE ----------------

def menu(phonebook):

    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display Contacts")
        print("6. Run Tests")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            print(add_contact(phonebook, name, phone))

        elif choice == "2":
            name = input("Enter name: ")
            print(search_contact(phonebook, name))

        elif choice == "3":
            name = input("Enter name: ")
            phone = input("Enter new phone number: ")
            print(update_contact(phonebook, name, phone))

        elif choice == "4":
            name = input("Enter name: ")
            print(delete_contact(phonebook, name))

        elif choice == "5":
            phonebook.display()

        elif choice == "6":
            run_tests(phonebook)

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


# ---------------- MAIN ----------------

phonebook = HashTable()
menu(phonebook)
