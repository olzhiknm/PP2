import os
import math
import time
import functools
def multiply_list(lst):
    return functools.reduce(lambda x, y: x * y, lst, 1)
def count_case_letters(text):
    return sum(map(str.isupper, text)), sum(map(str.islower, text))
def is_palindrome(text):
    return text == text[::-1]
def delayed_sqrt(number, delay):
    time.sleep(delay / 1000)
    return math.sqrt(number)
def all_elements_true(tpl):
    return all(tpl)
