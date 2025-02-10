from django.http import JsonResponse
from rest_framework.views import APIView
from .crawler import fetch_latest_lotto_data
from .models import LottoData
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import LottoData
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recommendation, LottoData

class CheckResultsView(APIView):
    def get(self, request):
        user = request.user
        recommendations = Recommendation.objects.filter(user=user)
        results = []

        for rec in recommendations:
            lotto = LottoData.objects.filter(draw_number=rec.draw_number).first()
            if lotto:
                winning_numbers = [lotto.num_1, lotto.num_2, lotto.num_3, lotto.num_4, lotto.num_5, lotto.num_6]
                match_count = len(set(rec.recommended_numbers) & set(winning_numbers))
                rec.match_count = match_count
                rec.save()
                results.append({
                    "draw_number": rec.draw_number,
                    "recommended_numbers": rec.recommended_numbers,
                    "match_count": match_count,
                })

        return Response(results)

class RecommendNumbersView(APIView):
    def get(self, request, strategy):
        if strategy == "1":  # 전략 1: 많이 나온 번호 추천
            data = LottoData.objects.all()
        elif strategy == "2":  # 전략 2: 적게 나온 번호 추천 (최근 3년)
            recent_draws = LottoData.objects.order_by('-draw_number')[:156]  # 3년 = 약 156회
            data = recent_draws
        else:
            return Response({"error": "Invalid strategy"}, status=400)

        # 번호 출현 횟수 계산
        all_numbers = []
        for lotto in data:
            all_numbers.extend([lotto.num_1, lotto.num_2, lotto.num_3, lotto.num_4, lotto.num_5, lotto.num_6])
        number_counts = {i: all_numbers.count(i) for i in range(1, 46)}

        if strategy == "1":
            sorted_numbers = sorted(number_counts, key=number_counts.get, reverse=True)[:6]
        else:
            sorted_numbers = sorted(number_counts, key=number_counts.get)[:6]

        return Response({"recommended_numbers": sorted_numbers}, status=200)

class UpdateLottoDataView(APIView):
    def post(self, request):
        try:
            data = fetch_latest_lotto_data()
            draw_number = data["draw_number"]

            if LottoData.objects.filter(draw_number=draw_number).exists():
                return JsonResponse({"message": "이미 최신 데이터가 저장되어 있습니다."}, status=200)

            LottoData.objects.create(
                draw_number=draw_number,
                num_1=data["winning_numbers"][0],
                num_2=data["winning_numbers"][1],
                num_3=data["winning_numbers"][2],
                num_4=data["winning_numbers"][3],
                num_5=data["winning_numbers"][4],
                num_6=data["winning_numbers"][5],
                bonus_number=data["bonus_number"]
            )
            return JsonResponse({"message": "로또 데이터가 성공적으로 업데이트되었습니다."}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        


class LuckyNumber(APIView):
    pass