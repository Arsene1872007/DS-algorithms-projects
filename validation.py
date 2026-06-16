def strip_non_digits(text):
    return "".join(ch for ch in text if ch.isdigit())


def validate_phone(phone_no):
    return phone_no.isdigit() and len(phone_no) >= 10


def validate_name(name):
    return bool(name.strip()) and all(
        c.isalpha() or c in " -" for c in name
    )
