from pathlib import Path

from games.anagrams import generate_anagrams

BASE_DIR = Path(__file__).resolve().parent.parent


def run(*args):

    regex_match = r"^[A-Za-z]+$"
    line_break_symbol = "\n"

    ANAGRAMS = generate_anagrams(*args, regex_match, line_break_symbol)

    f = open(f"{BASE_DIR}/games/games/anagrams/anagrams.py", "w")
    f.write(f"ANAGRAMS = {ANAGRAMS}")
    f.close()
