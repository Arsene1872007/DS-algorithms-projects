import re


def validate_phone(phone_no):
    checkdigits = re.sub(r"[\s\-\+]", "", phone_no)
    return checkdigits.isdigit() and len(checkdigits) >= 10


def validate_name(name):
    return bool(name.strip()) and all(
        c.isalpha() or c in " -" for c in name
    )
