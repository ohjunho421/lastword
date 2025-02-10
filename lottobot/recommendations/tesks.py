import pandas as pd
import numpy as np
import joblib
from .models import LottoData

# 머신러닝 모델 로드
model = joblib.load("ml_model.pkl")

# 과거 데이터 기반 전략 (전략 1)
def recommend_high_frequency_numbers_with_ml(data):
    all_numbers = data[["num_1", "num_2", "num_3", "num_4", "num_5", "num_6"]].values.flatten()
    number_counts = pd.Series(all_numbers).value_counts()
    machine_learning_numbers = get_ml_recommended_numbers(data)

    # 머신러닝 추천 번호와 많이 나온 번호 조합
    high_frequency_numbers = number_counts[number_counts > number_counts.mean()].index
    combined_numbers = list(set(high_frequency_numbers) & set(machine_learning_numbers))
    return sorted(combined_numbers[:6])

# 최근 데이터 기반 전략 (전략 2)
def recommend_low_frequency_numbers_with_ml(data):
    all_numbers = data[["num_1", "num_2", "num_3", "num_4", "num_5", "num_6"]].values.flatten()
    number_counts = pd.Series(all_numbers).value_counts()
    machine_learning_numbers = get_ml_recommended_numbers(data)

    # 머신러닝 추천 번호와 적게 나온 번호 조합
    low_frequency_numbers = number_counts[number_counts < number_counts.mean()].index
    combined_numbers = list(set(low_frequency_numbers) & set(machine_learning_numbers))
    return sorted(combined_numbers[:6])

# 머신러닝 추천 번호 추출
def get_ml_recommended_numbers(data):
    recent_data = data.tail(156)  # 최근 3년 기준
    recent_X = recent_data[["num_1", "num_2", "num_3", "num_4", "num_5", "num_6"]]
    predictions = model.predict_proba(recent_X)

    probabilities = np.mean(predictions, axis=0)
    machine_learning_numbers = np.argsort(probabilities)[-6:] + 1
    return machine_learning_numbers