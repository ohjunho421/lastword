from django.urls import path
from .views import UpdateLottoDataView, RecommendNumbersView, CheckResultsView

urlpatterns = [
    path('update-lotto-data/', UpdateLottoDataView.as_view(), name='update_lotto_data'),
    path('recommend/<str:strategy>/', RecommendNumbersView.as_view(), name='recommend_numbers'),
    path('check-results/', CheckResultsView.as_view(), name='check_results'),
]