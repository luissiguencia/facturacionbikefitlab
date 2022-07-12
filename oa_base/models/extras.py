# -*- coding: utf-8 -*-
"""Extra validations module"""
import re


def validate_partner_name(name):
    """Validate the name of a partner

    Args:
        name (char): [the name to validate]

    Returns:
        True: if name is correct
        False: Otherwise
    """
    special_characters = '''!@#$%^&*()-+?_=,<>/'''
    if len(name) <= 4:
        return False
    if name.isdigit():
        return False
    for character in name:
        if character in special_characters:
            return False
    return True

def validate_email_address(email):
    """Validate the email address

    Args:
        email (char): [the email to validate]

    Returns:
        True: if email is correct
        False: Otherwise
    """
    if len(email) > 7:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            #if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
            if ',' in email:
                return False
            if '<' in email:
                return False
            if '>' in email:
                return False
            if ';' in email:
                return False
            return True
    return False
