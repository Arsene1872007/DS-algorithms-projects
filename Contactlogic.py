import re
class Contact:
    def __init__(self,name,phone_no):
        self.name=name
        self.phone_no=phone_no
        self.next=None
        
def validate_phone(phone_no):
    checkdigits=re.sub(r"[\s\-\+]", "", phone_no)
    return checkdigits.isdigit() and len(checkdigits)>=10


def validate_name(name):
    return bool(name.strip()) and all(c.isalpha()or c in " -" for c in name)

def add_contact(hash_table,name,phone_no):
    if not validate_name(name):
        return "Invalid name"
    if not validate_phone(phone_no):
        return "Invalid phone number"
    if hash_table.search(name):#bach search in the hashtable
        return f"Contact '{name}' alraedy exists"
    hash_table.insert(name,phone_no)
    return f"Contact '{name}' added successfully"

def search_contact(hash_table,name):
    contact = hash_table.search(name)
    if not contact:
        return f"Contact '{name}' not found"
    return f"Name: {contact.name} | phone: {contact.phone_no}"

def delete_contact(hash_table,name):
    if not hash_table.search(name):
        return f"Contact '{name}' not found"
    hash_table.delete(name)
    return f"Contact '{name}' deleted successfully"

def update_contact(hash_table,name,new_phone_no):
    if not validate_phone(new_phone_no):
        return "Invalid phone number"
    contact=hash_table.search(name)
    if not contact:
        return f"Contact '{name}'not found "
    contact.phone_no=new_phone_no
    return f"Contact '{name}' updated successfully"
    
    
