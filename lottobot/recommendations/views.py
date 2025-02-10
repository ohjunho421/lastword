from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import recommend_high_frequency_numbers_with_ml, recommend_low_frequency_numbers_with_ml
from .models import LottoData, Recommendation
import pandas as pd

def load_lotto_data():
    data = LottoData.objects.all().values("num_1", "num_2", "num_3", "num_4", "num_5", "num_6")
    return pd.DataFrame(list(data))

class ChatBotRecommendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        strategy = request.data.get("strategy")  # 입력된 전략 번호

        # 데이터 로드
        data = load_lotto_data()

        # 전략별 추천 번호 생성
        if strategy == "1":
            numbers = recommend_high_frequency_numbers_with_ml(data)
        elif strategy == "2":
            numbers = recommend_low_frequency_numbers_with_ml(data)
        else:
            return Response({"error": "Invalid strategy. Choose '1' or '2'."}, status=400)

        # 추천 기록 저장
        Recommendation.objects.create(
            user=user,
            strategy=strategy,
            recommended_numbers=numbers,
        )

        return Response({"recommended_numbers": numbers}, status=200)