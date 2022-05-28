from decimal import Decimal

from django.db import models
from django.db.models import Count, DecimalField, ExpressionWrapper, F, FloatField
from django.db.models.functions import Round
from django_cte import CTEQuerySet, With


class GameRecordQueryset(CTEQuerySet):
    def plot_chart(self):
        cte = With(self.model.objects.values("game").annotate(total=Count("score")))

        games = (
            cte.join(self.model.objects.values("game", "score"), game=cte.col.game)
            .with_cte(cte)
            .annotate(total_per_score=Count("score"))
            .annotate(total=cte.col.total)
            .annotate(
                percentage=ExpressionWrapper(
                    Round(F("total_per_score") * Decimal("1.0") / F("total") * 100, precision=2),
                    output_field=DecimalField(),
                )
            )
            .order_by("score")
        )

        return games


class GameRecord(models.Model):
    games = [
        ("OOO", "Odd One Out"),
        ("A", "Anagrams"),
        ("K", "Keypad"),
    ]
    game = models.CharField(choices=games, max_length=3)
    score = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    # add user ?

    objects = GameRecordQueryset.as_manager()
