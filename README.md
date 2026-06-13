# Phonebook Project

A command-line phonebook application built in Python using a **hash table** for fast contact lookups and a **linked list** for collision chaining within each bucket.

---

## Project Structure

```
phonebook-project/
├── phonebook_main.py   # Entry point — menu UI and test suite
├── hashtable.py        # HashTable class — connector between all modules
├── Linked_List.py      # LinkedList and Node classes — bucket ordering
├── Contactlogic.py     # Business logic — add, search, update, delete
└── validation.py       # Input validation — name and phone number rules
```

### How the files connect

```
phonebook_main.py
        │
        ▼
  Contactlogic.py  ──── validation.py
        │
        ▼
   hashtable.py
        │
        ▼
  Linked_List.py
```

- **`phonebook_main.py`** is the entry point. It drives the menu and calls `Contactlogic` functions.
- **`Contactlogic.py`** owns the business logic (validation checks, duplicate checks, not-found checks). It calls into `HashTable`.
- **`hashtable.py`** is the connector. It uses `LinkedList` per bucket for chaining and exposes the storage interface that `Contactlogic` depends on.
- **`Linked_List.py`** handles ordering within each hash bucket (collision resolution via chaining).
- **`validation.py`** enforces name and phone number rules before any contact is stored.

---

## Features

- Add a contact (name + phone number)
- Search for a contact by name
- Update a contact's phone number
- Delete a contact
- Display all contacts
- Built-in test suite

---

## How to Run

Make sure you have **Python 3** installed, then run:

```bash
python phonebook_main.py
```

You will see the following menu:

```
===== PHONEBOOK MENU =====
1. Add Contact
2. Search Contact
3. Update Contact
4. Delete Contact
5. Display Contacts
6. Run Tests
7. Exit
```

---

## Input Rules

**Name**
- Must not be empty
- Only letters, spaces (`" "`), and hyphens (`"-"`) are allowed
- Examples: `Alice`, `Mary-Jane`, `John Smith`

**Phone Number**
- Must contain at least 10 digits
- Spaces, dashes (`-`), and plus signs (`+`) are stripped before validation
- Examples: `0781234567`, `+1 800-555-0199`

---

## Data Structure Design

### Hash Table (`hashtable.py`)

The `HashTable` uses a simple hash function:

```python
sum(ord(char) for char in key.lower()) % size
```

Default size is 10 buckets. Each bucket holds a `LinkedList` for chaining when multiple names hash to the same index.

A `_contacts` dictionary (`name.lower()` → `Contact`) stores live object references so that in-place updates (e.g. `contact.phone_no = new_value`) are reflected immediately without re-inserting.

### Linked List (`Linked_List.py`)

Each bucket in the hash table is a `LinkedList`. When two contacts hash to the same bucket, they are chained as nodes in that list, preserving insertion order.

### Contact (`hashtable.py`)

```python
class Contact:
    name: str
    phone_no: str
```

---

## Example Usage (via menu)

```
Choose an option: 1
Enter name: Alice
Enter phone number: 0781234567
Contact 'Alice' added successfully

Choose an option: 2
Enter name: Alice
Name: Alice | Phone: 0781234567

Choose an option: 3
Enter name: Alice
Enter new phone number: 0700000000
Contact 'Alice' updated successfully

Choose an option: 4
Enter name: Alice
Contact 'Alice' deleted successfully
```

---

## Running the Test Suite

Select option `6` from the menu to run the built-in tests. The suite covers:

- Adding valid contacts
- Searching for an existing contact
- Updating a contact's phone number
- Deleting a contact
- Searching for a deleted contact (should return not found)
- Adding a contact with an invalid name (empty)
- Adding a contact with an invalid phone number (too short)
