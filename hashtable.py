class Contact:
    def __init__(self, name, phone_no):
        self.name = name
        self.phone_no = phone_no
        self.next = None


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
