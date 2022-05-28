from django.urls import path

from .views import (
    get_anagrams_game,
    get_anagrams_practice_game,
    get_bell_curve,
    get_odd_one_out_game,
    get_odd_one_out_practice_game,
    record_game,
)

app_name = "games"
urlpatterns = [
    path("anagrams/practice", get_anagrams_practice_game, name="get_anagrams_practice_game"),
    path("anagrams/game", get_anagrams_game, name="get_anagrams_game"),
    path(
        "odd_one_out/practice", get_odd_one_out_practice_game, name="get_odd_one_out_practice_game"
    ),
    path("odd_one_out/game", get_odd_one_out_game, name="get_odd_one_out_game"),
    path("get_bell_curve", get_bell_curve, name="get_bell_curve"),
    path("record_game", record_game, name="record_game"),
]
