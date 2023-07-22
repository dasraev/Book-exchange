from django import template
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
register = template.Library()


def extract_emails(name):
    email_list = name.split('-')
    valid_emails = [email for email in email_list if is_valid_email(email)]
    return valid_emails

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# Test the function

@register.filter
def get_email(value,email):
    print(145,value)
    valid_emails = extract_emails(value)
    print(146,valid_emails)
    valid_emails.remove(email)
    print(147,valid_emails)
    return valid_emails[0]

@register.filter
def group_name(value,email):
    print(909,f'{min(value,email)}-{max(value,email)}')
    return f'{min(value,email)}-{max(value,email)}'
