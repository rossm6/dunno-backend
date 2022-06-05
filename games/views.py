from random import sample
import copy

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from games.games.anagrams.anagrams import ANAGRAMS
from games.games.odd_one_out.n_3 import GAMES as N_3_GAMES
from games.models import GameRecord
from games.utils import caesar_cipher, pick_n_random, true_shuffle

"""
Graphql is overkill for this project.
And DRF isn't much better.
"""

CAESAR_CIPHER_SHIFT = 67


def get_points(points):
    return [{"score": point["score"], "percentage": point["percentage"], "total": point["total"]} for point in points]


def get_bell_curve(request):
    game = request.GET.get("game")
    # filter must come after plot_chart
    # TODO - see if this can be avoided
    points = GameRecord.objects.plot_chart().filter(game=game)
    data = {"points": get_points(points)}
    return JsonResponse(data=data)


def shuffle_game(game):
    """
    Increase the number of possible games by shuffing the squares.
    This way we also make the correct answer more random.
    """
    odd_one_out_index = game["game"]["odd_one_out_index"]
    odd_one_out_square = game["game"]["squares"][odd_one_out_index]

    true_shuffle(game["game"]["squares"])

    for i, square in enumerate(game["game"]["squares"]):
        if square == odd_one_out_square:
            game["game"]["odd_one_out_index"] = i
            break


START_ANAGRAM_WORD_LENGTH = 2
END_ANAGRAM_WORD_LENGTH = 15
PRACTICE_ANAGRAM_WORD_LENGTH = 3


def pick_random_word(words):
    return sample(words, 1)[0]


def get_anagram_and_solution_from_word(word):
    word_as_list = list(word)
    true_shuffle(word_as_list)
    anagram = "".join(word_as_list)
    return {"anagram": anagram, "solution": word}


def get_anagrams_practice_game(request):
    words = ANAGRAMS[PRACTICE_ANAGRAM_WORD_LENGTH]
    word = pick_random_word(words)
    practice_anagram = get_anagram_and_solution_from_word(word)
    practice_anagram["solution"] = caesar_cipher(practice_anagram["solution"], CAESAR_CIPHER_SHIFT)
    return JsonResponse(data={"games": [practice_anagram]})


def get_anagrams_game(request):
    anagrams = {}

    for word_length in range(2, END_ANAGRAM_WORD_LENGTH + 1):
        words = ANAGRAMS[word_length]
        word = pick_random_word(words)
        anagram = get_anagram_and_solution_from_word(word)
        anagrams[word_length] = anagram
        anagram["solution"] = caesar_cipher((anagram["solution"]), CAESAR_CIPHER_SHIFT)

    return JsonResponse(data={"games": list(anagrams.values())})


def get_odd_one_out_practice_game(request):
    data = {}
    games = []

    n_3_level_1 = [copy.deepcopy(game) for game in N_3_GAMES if game["level"] == 1]
    n_3_level_2 = [copy.deepcopy(game) for game in N_3_GAMES if game["level"] == 2]

    games = games + [
        {"n": 3, "game": game}
        for game in pick_n_random(n_3_level_1, 1) + pick_n_random(n_3_level_2, 1)
    ]

    for game in games:
        shuffle_game(game)
        game["game"]["odd_one_out_index"] = caesar_cipher(
            str(game["game"]["odd_one_out_index"]), CAESAR_CIPHER_SHIFT
        )

    data["games"] = games

    return JsonResponse(data=data)


def get_odd_one_out_game(request):
    data = {}
    games = []

    n_3_level_1 = [copy.deepcopy(game) for game in N_3_GAMES if game["level"] == 1]
    n_3_level_2 = [copy.deepcopy(game) for game in N_3_GAMES if game["level"] == 2]

    games = games + [
        {"n": 3, "game": game}
        for game in pick_n_random(n_3_level_1, 5) + pick_n_random(n_3_level_2, 30)
    ]

    for game in games:
        shuffle_game(game)
        game["game"]["odd_one_out_index"] = caesar_cipher(
            str(game["game"]["odd_one_out_index"]), CAESAR_CIPHER_SHIFT
        )

    data["games"] = games

    return JsonResponse(data=data)


@require_http_methods(["POST"])
def record_game(request):
    game = request.POST.get("game")
    score = request.POST.get("score")
    score = int(score)
    record = GameRecord.objects.create(game=game, score=score)
    points = GameRecord.objects.plot_chart().filter(game=game)
    points = get_points(points)

    return JsonResponse(
        {
            "bellCurve": {
                "points": points,
                "you": {
                    "score": record.score,
                    "percentile": (
                        int(
                            sum(
                                [
                                    point["percentage"]
                                    for point in points
                                    if point["score"] <= record.score
                                ]
                            )
                        )
                    ),
                },
            }
        }
    )
