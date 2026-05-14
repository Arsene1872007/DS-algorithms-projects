#!/usr/bin/env python3
"""
Contact Book - A simple CLI contact manager.
Stores contacts as JSON. Supports add, search, delete, and list.
"""

import json
import os
import sys

CONTACTS_FILE = "contacts.json"


# ── Persistence ──────────────────────────────────────────────────────────────

def load_contacts() -> list[dict]:
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_contacts(contacts: list[dict]) -> None:
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)


# ── Core operations ───────────────────────────────────────────────────────────

def add_contact(name: str, phone: str, email: str, address: str = "") -> dict:
    """Add a new contact and return it."""
    contacts = load_contacts()

    # Prevent exact duplicate names
    if any(c["name"].lower() == name.lower() for c in contacts):
        raise ValueError(f"A contact named '{name}' already exists.")

    contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    }
    contacts.append(contact)
    save_contacts(contacts)
    return contact


def search_contacts(query: str) -> list[dict]:
    """Return contacts whose name, phone, email, or address contain query."""
    q = query.lower()
    return [
        c for c in load_contacts()
        if q in c["name"].lower()
        or q in c["phone"].lower()
        or q in c["email"].lower()
        or q in c.get("address", "").lower()
    ]


def delete_contact(name: str) -> bool:
    """Delete a contact by exact name (case-insensitive). Returns True if deleted."""
    contacts = load_contacts()
    new_contacts = [c for c in contacts if c["name"].lower() != name.lower()]
    if len(new_contacts) == len(contacts):
        return False
    save_contacts(new_contacts)
    return True


def list_contacts() -> list[dict]:
    """Return all contacts sorted by name."""
    return sorted(load_contacts(), key=lambda c: c["name"].lower())


# ── Display helpers ───────────────────────────────────────────────────────────

DIVIDER = "─" * 50

def print_contact(c: dict) -> None:
    print(f"  Name   : {c['name']}")
    print(f"  Phone  : {c['phone']}")
    print(f"  Email  : {c['email']}")
    if c.get("address"):
        print(f"  Address: {c['address']}")


def print_contacts(contacts: list[dict], header: str = "") -> None:
    if header:
        print(f"\n{header}")
    if not contacts:
        print("  (no contacts found)")
        return
    for c in contacts:
        print(DIVIDER)
        print_contact(c)
    print(DIVIDER)
    print(f"  {len(contacts)} contact(s) total.\n")


# ── Interactive prompts ───────────────────────────────────────────────────────

def prompt(label: str, required: bool = True) -> str:
    while True:
        value = input(f"  {label}: ").strip()
        if value or not required:
            return value
        print(f"  ✗  {label} is required.")


def interactive_add() -> None:
    print("\n── Add Contact ─────────────────────────────────")
    name    = prompt("Name")
    phone   = prompt("Phone")
    email   = prompt("Email")
    address = prompt("Address (optional, press Enter to skip)", required=False)
    try:
        contact = add_contact(name, phone, email, address)
        print(f"\n  ✓  Contact '{contact['name']}' saved.\n")
    except ValueError as e:
        print(f"\n  ✗  {e}\n")


def interactive_search() -> None:
    print("\n── Search Contacts ─────────────────────────────")
    query = prompt("Search query")
    results = search_contacts(query)
    print_contacts(results, header=f"Results for '{query}':")


def interactive_delete() -> None:
    print("\n── Delete Contact ──────────────────────────────")
    name = prompt("Exact name to delete")
    confirm = input(f"  Delete '{name}'? [y/N] ").strip().lower()
    if confirm != "y":
        print("  Cancelled.\n")
        return
    if delete_contact(name):
        print(f"  ✓  '{name}' deleted.\n")
    else:
        print(f"  ✗  No contact named '{name}' found.\n")


def interactive_list() -> None:
    print_contacts(list_contacts(), header="── All Contacts ────────────────────────────────")


# ── Main menu ─────────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════╗
║       📒  Contact Book       ║
╠══════════════════════════════╣
║  1 · Add a contact           ║
║  2 · Search contacts         ║
║  3 · Delete a contact        ║
║  4 · Display all contacts    ║
║  5 · Quit                    ║
╚══════════════════════════════╝
"""

ACTIONS = {
    "1": interactive_add,
    "2": interactive_search,
    "3": interactive_delete,
    "4": interactive_list,
}


def main() -> None:
    while True:
        print(MENU)
        choice = input("  Choose an option [1-5]: ").strip()
        if choice == "5":
            print("  Bye! 👋\n")
            sys.exit(0)
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("  Invalid choice. Please enter 1–5.\n")


if __name__ == "__main__":
    main()
