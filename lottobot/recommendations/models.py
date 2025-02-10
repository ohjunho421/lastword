from django.db import models
from django.conf import settings

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    draw_number = models.IntegerField()
    recommended_numbers = models.JSONField()  # 추천 번호
    match_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class LottoData(models.Model):
    draw_number = models.IntegerField(unique=True)
    num_1 = models.IntegerField()
    num_2 = models.IntegerField()
    num_3 = models.IntegerField()
    num_4 = models.IntegerField()
    num_5 = models.IntegerField()
    num_6 = models.IntegerField()
    bonus_number = models.IntegerField()

    def __str__(self):
        return f"Draw {self.draw_number}: {self.num_1}, {self.num_2}, {self.num_3}, {self.num_4}, {self.num_5}, {self.num_6} + {self.bonus_number}"