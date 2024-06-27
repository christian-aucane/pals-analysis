import re
import logging


LOGGER = logging.getLogger("REGEX")


def remove_special_characters(string, replace_with=""):
    return re.sub(r'[^a-zA-Z0-9]', replace_with, string)

def camel_case_to_snake_case(string):
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', string)

def normalize_special_cases(string: str, special_cases: dict = {}):
    # TODO : optimize this function
    
    for case, replacement in special_cases.items():
        if case.lower() in string.lower():
            LOGGER.debug("Special case found: %s", case)
            string = re.sub(r'\b{}\b'.format(re.escape(case)), replacement, string, flags=re.IGNORECASE)
    
    return string
