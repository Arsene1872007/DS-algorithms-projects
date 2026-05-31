class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [None] * size

    def hash_function(self, key):
        """Convert key into a bucket index."""
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)

        # Empty bucket
        if self.buckets[index] is None:
            self.buckets[index] = Node(key, value)
            return

        # Check if key exists or move to end
        current = self.buckets[index]

        while True:
            if current.key == key:
                current.value = value  # Update existing key
                return

            if current.next is None:
                break

            current = current.next

        # Collision: add new node to linked list
        current.next = Node(key, value)

    def search(self, key):
        index = self.hash_function(key)
        current = self.buckets[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def delete(self, key):
        index = self.hash_function(key)
        current = self.buckets[index]
        previous = None

        while current:
            if current.key == key:
                if previous is None:
                    self.buckets[index] = current.next
                else:
                    previous.next = current.next
                return True

            previous = current
            current = current.next

        return False

    def display(self):
        for i in range(self.size):
            print(f"Bucket {i}:", end=" ")

            current = self.buckets[i]
            while current:
                print(f"({current.key}: {current.value})", end=" -> ")
                current = current.next

            print("None")


# Example Usage
phonebook = HashTable()

phonebook.insert("Alice", "123456789")
phonebook.insert("Bob", "987654321")
phonebook.insert("Charlie", "555666777")

print("Alice:", phonebook.search("Alice"))
print("Bob:", phonebook.search("Bob"))

phonebook.display()
