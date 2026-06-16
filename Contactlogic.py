from validation import validate_phone, validate_name


def add_contact(hash_table, name, phone_no):
    if not validate_name(name):
        return "Invalid name"
    if not validate_phone(phone_no):
        return "Invalid phone number"
    hash_table.insert(name, phone_no)
    return f"Contact '{name}' added successfully"


def search_contact(hash_table, name):
    contacts = hash_table.search(name)
    if not contacts:
        return f"Contact '{name}' not found"
    return "\n".join(f"Name: {c.name} | Phone: {c.phone_no}" for c in contacts)


def delete_contact(hash_table, name, phone_no):
    if not hash_table.search(name):
        return f"Contact '{name}' not found"
    if not hash_table.delete(name, phone_no):
        return f"No contact '{name}' with phone '{phone_no}' found"
    return f"Contact '{name}' with phone '{phone_no}' deleted successfully"


def update_contact(hash_table, name, old_phone_no, new_phone_no):
    if not validate_phone(new_phone_no):
        return "Invalid phone number"
    contacts = hash_table.search(name)
    for contact in contacts:
        if contact.phone_no == old_phone_no:
            contact.phone_no = new_phone_no
            return f"Contact '{name}' updated successfully"
    return f"No contact '{name}' with phone '{old_phone_no}' found"
