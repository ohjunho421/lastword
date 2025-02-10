from django.db import models
from django.conf import settings

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
        return f"Draw {self.draw_number}"

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    strategy = models.CharField(max_length=10)  # 사용한 전략 (1, 2)
    recommended_numbers = models.JSONField()  # 추천 번호 리스트
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation by {self.user} ({self.strategy})"