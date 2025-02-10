from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import recommend_high_frequency_numbers_with_ml, recommend_low_frequency_numbers_with_ml
from .models import LottoData, Recommendation
import pandas as pd

def load_lotto_data():
    """
    LottoData 모델 데이터를 Pandas DataFrame으로 로드.
    """
    data = LottoData.objects.all().values("num_1", "num_2", "num_3", "num_4", "num_5", "num_6")
    if not data:
        raise ValueError("LottoData에 데이터가 없습니다.")
    return pd.DataFrame(list(data))

class ChatBotRecommendView(APIView):
    """
    전략에 따라 로또 번호를 추천하는 APIView.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        strategy = request.data.get("strategy")  # 입력된 전략 번호

        try:
            # 데이터 로드
            data = load_lotto_data()

            # 전략별 추천 번호 생성
            if strategy == "1":
                task = recommend_high_frequency_numbers_with_ml.delay(data.to_dict())
            elif strategy == "2":
                task = recommend_low_frequency_numbers_with_ml.delay(data.to_dict())
            else:
                return Response({"error": "Invalid strategy. Choose '1' or '2'."}, status=400)

            # Celery 작업 결과 상태 반환
            Recommendation.objects.create(
                user=user,
                strategy=strategy,
                recommended_numbers=None,  # Celery 작업 결과가 완료되기 전이므로 None
            )

            return Response({
                "message": "추천 작업이 요청되었습니다. 결과는 별도로 확인하십시오.",
                "task_id": task.id,
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)