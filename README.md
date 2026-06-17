# Phonebook Project

A phonebook application built in Python using a **hash table** for fast contact lookups and **linked list chaining** for collision resolution. Comes with both a command-line interface and a graphical user interface.

---

## Project Structure

```
phonebook-project/
├── phonebook_main.py   # Entry point — CLI menu and test suite
├── phonebook_gui.py    # GUI — built with CustomTkinter
├── hashtable.py        # HashTable and Contact classes
├── Contactlogic.py     # Business logic — add, search, update, delete
└── validation.py       # Input validation — name and phone number rules
```

### How the files connect

```
phonebook_main.py        phonebook_gui.py
        │                       │
        └──────────┬────────────┘
                   ▼
            Contactlogic.py ──── validation.py
                   │
                   ▼
             hashtable.py
```

- **`phonebook_main.py`** is the CLI entry point. It creates the `HashTable` instance and drives the menu.
- **`phonebook_gui.py`** is the GUI entry point. It creates its own `HashTable` instance and handles user interaction visually.
- **`Contactlogic.py`** owns the business logic — duplicate checks, not-found checks, and validation. It receives the hash table as a parameter and calls its methods.
- **`hashtable.py`** stores all contacts. Each bucket is a chain of `Contact` nodes linked via `next` pointers.
- **`validation.py`** enforces name and phone number rules before any contact is stored.

---

## Features

- Add a contact (name + phone number)
- Search for a contact by name
- Update a contact's phone number
- Delete a contact by name and phone number
- Display all contacts
- Support for multiple contacts with the same name (different numbers)
- Built-in test suite (CLI)
- Real-time digit-only enforcement on phone input (GUI)

---

## How to Run

Make sure you have **Python 3** installed.

**CLI:**
```bash
python phonebook_main.py
```

**GUI:**
```bash
python phonebook_gui.py
```

The GUI requires `customtkinter`:
```bash
pip install customtkinter
```

**CLI Menu:**
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
- Must not be empty or whitespace only
- Only letters, spaces (`" "`), and hyphens (`"-"`) are allowed
- Examples: `Alice`, `Mary-Jane`, `John Smith`

**Phone Number**
- Must contain digits only
- Must be at least 10 digits long
- Examples: `0781234567`, `07812345678`
- In the GUI, non-digit characters are stripped automatically as you type

---

## Data Structure Design

### Hash Table (`hashtable.py`)

The `HashTable` uses a hash function that converts a name into a bucket index:

```python
sum(ord(char) for char in key.lower()) % size
```

Default size is 10 buckets. Each bucket is either `None` or the head of a linked list of `Contact` nodes.

```
buckets[0] → Contact("Alice") → None
buckets[1] → None
buckets[2] → Contact("Bob") → Contact("Charlie") → None  ← collision chained
```

### Linked List Chaining (`hashtable.py`)

Collisions are resolved by chaining — when two contacts hash to the same bucket, the new contact is appended to the end of the existing chain via the `Contact.next` pointer. No data is ever overwritten.

### Contact Node (`hashtable.py`)

```python
class Contact:
    name: str
    phone_no: str
    next: Contact   # pointer to next node in the chain
```

---

## Example Usage (CLI)

```
Choose an option: 1
Enter name: Alice
Enter phone number: 0781234567
Contact 'Alice' added successfully

Choose an option: 1
Enter name: Alice
Enter phone number: 0700000000
Contact 'Alice' added successfully   ← same name, different number allowed

Choose an option: 2
Enter name: Alice
Name: Alice | Phone: 0781234567
Name: Alice | Phone: 0700000000

Choose an option: 3
Enter name: Alice
Enter current phone number: 0781234567
Enter new phone number: 0799999999
Contact 'Alice' updated successfully

Choose an option: 4
Enter name: Alice
Enter phone number: 0700000000
Contact 'Alice' with phone '0700000000' deleted successfully
```

---

## Running the Test Suite

Select option `6` from the CLI menu to run the built-in tests. The suite covers:

- Adding valid contacts
- Adding a second contact with the same name (different number)
- Searching for a contact (returns all matches)
- Updating a contact's phone number
- Deleting one contact by name and phone (other contacts with same name remain)
- Searching for a deleted contact (returns not found)
- Adding a contact with an invalid name (empty)
- Adding a contact with an invalid phone number (too short)
