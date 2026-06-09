from Linked_List import LinkedList
from Contactlogic import add_contact, search_contact, delete_contact, update_contact


class Contact:
    def __init__(self, name, phone_no):
        self.name = name
        self.phone_no = phone_no


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [LinkedList() for _ in range(size)]
        self._contacts = {}  # name.lower() -> live Contact object

    def hash_function(self, key):
        return sum(ord(char) for char in key.lower()) % self.size

    # --- Low-level interface (called by Contactlogic functions) ---

    def insert(self, name, phone_no):
        key = name.lower()
        if key in self._contacts:
            self._contacts[key].phone_no = phone_no
        else:
            index = self.hash_function(name)
            self._contacts[key] = Contact(name, phone_no)
            self.buckets[index].insert(name)

    def search(self, name):
        return self._contacts.get(name.lower())

    def delete(self, name):
        key = name.lower()
        if key not in self._contacts:
            return False
        index = self.hash_function(name)
        original_name = self._contacts[key].name
        self.buckets[index].delete(original_name)
        del self._contacts[key]
        return True

    # --- High-level interface (connector to Contactlogic) ---

    def add_contact(self, name, phone_no):
        return add_contact(self, name, phone_no)

    def search_contact(self, name):
        return search_contact(self, name)

    def delete_contact(self, name):
        return delete_contact(self, name)

    def update_contact(self, name, new_phone_no):
        return update_contact(self, name, new_phone_no)

    def display(self):
        print("\n----- PHONEBOOK -----")
        empty = True
        for i in range(self.size):
            cur = self.buckets[i].head
            while cur:
                contact = self._contacts.get(cur.data.lower())
                if contact:
                    print(f"Name: {contact.name} | Phone: {contact.phone_no}")
                    empty = False
                cur = cur.next
        if empty:
            print("Phonebook is empty.")
        print("---------------------")
