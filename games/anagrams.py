import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_words(path, regex_match, line_break_symbol):
    words = []
    path = BASE_DIR.joinpath(path)
    f = open(path, "r")
    for line in f:
        word = re.sub(re.escape(line_break_symbol), "", line)
        if re.search(regex_match, word):
            words.append(word)
    f.close()
    return words


def remove_anagrams_with_multiple_solutions(words):
    words_by_length = {}
    for word in words:
        if len(word) in words_by_length:
            words_by_length[len(word)].append(word)
        else:
            words_by_length[len(word)] = [word]

    checked = []

    for word_length, words in words_by_length.items():
        for word in words:
            letter_combination_unique = True
            for _word in words:
                if _word != word:
                    # comparing different words
                    if set(word) == set(_word):
                        letter_combination_unique = False
                        break

            if letter_combination_unique:
                checked.append(word)

    return checked


def generate_anagrams(path, regex_match, line_break_symbol):
    words = get_words(path, regex_match, line_break_symbol)
    words = remove_anagrams_with_multiple_solutions(words)
    words_by_length = {}
    reordered_keys = {}

    for word in words:
        if len(word) in words_by_length:
            words_by_length[len(word)].append(word)
        else:
            words_by_length[len(word)] = [word]

    for key in sorted(list(words_by_length.keys())):
        values = words_by_length[key]
        reordered_keys[key] = values

    return reordered_keys
