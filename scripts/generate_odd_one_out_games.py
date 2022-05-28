from pathlib import Path

from games.odd_one_out import generate_all_games as generate_all_odd_one_out_games

BASE_DIR = Path(__file__).resolve().parent.parent

MAX = 300


def run():

    GAMES = generate_all_odd_one_out_games(3, MAX)

    f = open(f"{BASE_DIR}/games/games/odd_one_out/n_3.py", "w")
    f.write(f"GAMES = {GAMES}")
    f.close()
