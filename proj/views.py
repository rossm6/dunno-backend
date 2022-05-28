from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

from games.views import CAESAR_CIPHER_SHIFT


def get_url(request, url_name):
    return request.build_absolute_uri(reverse(url_name))


@ensure_csrf_cookie
def init(request):

    data = {
        "urls": {
            "get_anagrams_practice_game": get_url(request, "games:get_anagrams_practice_game"),
            "get_anagrams_game": get_url(request, "games:get_anagrams_game"),
            "get_odd_one_out_game": get_url(request, "games:get_odd_one_out_game"),
            "get_odd_one_out_practice_game": get_url(
                request, "games:get_odd_one_out_practice_game"
            ),
            "get_bell_curve": get_url(request, "games:get_bell_curve"),
            "record_game": get_url(request, "games:record_game"),
        },
        "games": {"keypad": "K", "odd_one_out": "OOO", "anagram": "A"},
        "CAESAR_CIPHER_SHIFT": CAESAR_CIPHER_SHIFT,
    }

    return JsonResponse(data=data)
