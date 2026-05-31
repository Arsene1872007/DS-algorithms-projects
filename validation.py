import re

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


# ---------------- USER INTERFACE ----------------

def menu(phonebook):

    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display Contacts")
        print("6. Exit")

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
            print("Program terminated.")
            break

        else:
            print("Invalid option. Please try again.")


# ---------------- TEST CASES ----------------

def run_tests(phonebook):

    print("\n----- TESTING -----")

    print(add_contact(phonebook, "Alice", "1234567890"))
    print(add_contact(phonebook, "Bob", "9876543210"))

    print(search_contact(phonebook, "Alice"))

    print(update_contact(phonebook, "Alice", "1112223333"))
    print(search_contact(phonebook, "Alice"))

    print(delete_contact(phonebook, "Bob"))
    print(search_contact(phonebook, "Bob"))

    print(add_contact(phonebook, "", "1234567890"))
    print(add_contact(phonebook, "John", "123"))

    print("----- END OF TESTS -----\n")
