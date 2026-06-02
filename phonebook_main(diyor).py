from tamjit import HashTable
from Contactlogic import add_contact, search_contact, delete_contact, update_contact


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
