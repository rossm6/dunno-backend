from datetime import date
from random import sample, shuffle

from hashids import Hashids


def pick_n_random(li, n):
    random_indexes = sample(range(0, len(li)), n)
    return [li[i] for i in random_indexes]


def true_shuffle(li):
    orig = li.copy()
    if len(li) <= 1:
        return
    while orig == li:
        shuffle(li)
    return li


def shift(code, base, range, shiftValue):
    """
    This code matches the implementation on the clientside
    """
    modulus_result = (code - base + shiftValue) % range
    return (modulus_result + range if modulus_result < 0 else modulus_result) + base


def shifted(char, shiftValue):
    code = ord(char)
    if code >= 97 and code <= 122:
        return shift(code, 97, 122 - 97 + 1, shiftValue)
    elif code >= 65 and code <= 90:
        return shift(code, 65, 90 - 65 + 1, shiftValue)
    elif code >= 48 and code <= 57:
        return shift(code, 48, 57 - 48 + 1, shiftValue)


def caesar_cipher(text, shiftValue):
    return "".join([chr(code) for code in [shifted(char, shiftValue) for char in list(text)]])
