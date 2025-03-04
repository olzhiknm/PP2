import re

def match_a_followed_by_b(text):
    return re.fullmatch(r'ab*', text) is not None

def match_a_followed_by_2to3_b(text):
    return re.fullmatch(r'ab{2,3}', text) is not None

def find_lowercase_with_underscore(text):
    return re.findall(r'\b[a-z]+_[a-z]+\b', text)

def find_upper_followed_by_lower(text):
    return re.findall(r'\b[A-Z][a-z]+', text)

def match_a_anything_b(text):
    return re.fullmatch(r'a.*b', text) is not None

def replace_space_comma_dot(text):
    return re.sub(r'[\s,\.]', ':', text)

def snake_to_camel(text):
    return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(text.split('_')))

def split_at_uppercase(text):
    return re.split(r'(?=[A-Z])', text)

def insert_spaces_between_capitals(text):
    return re.sub(r'([A-Z])', r' \1', text).strip()

def camel_to_snake(text):
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', text).lower()
