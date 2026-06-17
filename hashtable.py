class Contact:
    # Creates a contact node holding a name and phone number, linked to the next node in its bucket.
    def __init__(self, name, phone_no):
        self.name = name
        self.phone_no = phone_no
        self.next = None


class HashTable:
    # Creates a hash table with a fixed number of empty buckets.
    def __init__(self, size=10):
        self.size = size
        self.buckets = [None] * size

    # Computes the bucket index for a key by summing character codes and taking the modulus of the table size.
    def hash_function(self, key):
        return sum(ord(char) for char in key.lower()) % self.size

    # Adds a new contact to the bucket for its name, appending to the end of any existing chain.
    def insert(self, name, phone_no):
        index = self.hash_function(name)
        new_contact = Contact(name, phone_no)

        if self.buckets[index] is None:
            self.buckets[index] = new_contact
            return

        current = self.buckets[index]
        while current.next:
            current = current.next
        current.next = new_contact

    # Finds all contacts matching the given name (case-insensitive) within its bucket's chain.
    def search(self, name):
        index = self.hash_function(name)
        current = self.buckets[index]
        results = []
        while current:
            if current.name.lower() == name.lower():
                results.append(current)
            current = current.next
        return results

    # Removes the contact matching the given name and phone number from its bucket's chain; returns True if removed, False if not found.
    def delete(self, name, phone_no):
        index = self.hash_function(name)
        current = self.buckets[index]
        previous = None
        while current:
            if current.name.lower() == name.lower() and current.phone_no == phone_no:
                if previous is None:
                    self.buckets[index] = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

    # Prints every contact in the phonebook, or a message if it's empty.
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
