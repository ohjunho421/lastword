from celery import shared_task
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from .crawler import crawl_latest_lotto  # 크롤링 함수 임포트

# Django 프로젝트의 BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CSV 및 모델 경로 설정
CSV_FILE_PATH = os.path.join(BASE_DIR, "로또봇.csv")
MODEL_FILE_PATH = os.path.join(BASE_DIR, "ml_model.pkl")


@shared_task
def update_lotto_data_and_retrain():
    """
    1. 최신 로또 데이터를 크롤링
    2. CSV 파일 업데이트
    3. 머신러닝 모델 재학습 및 저장
    """
    try:
        # 1. 최신 데이터 크롤링
        print("최신 데이터를 크롤링 중...")
        latest_data = crawl_latest_lotto()  # 크롤링 함수 호출
        if not latest_data:
            raise ValueError("크롤링된 데이터가 비어 있습니다.")
        print(f"크롤링된 데이터: {latest_data}")

        # 2. 기존 데이터 로드 또는 새로 생성
        try:
            data = pd.read_csv(CSV_FILE_PATH)
            print("기존 CSV 파일 로드 완료.")
        except FileNotFoundError:
            print("CSV 파일이 존재하지 않아 새로 생성합니다.")
            data = pd.DataFrame(columns=["날짜", "번호1", "번호2", "번호3", "번호4", "번호5", "번호6", "보너스"])

        # 3. 데이터 병합 및 중복 제거
        print("데이터 병합 및 중복 제거 중...")
        latest_df = pd.DataFrame([latest_data])
        updated_data = pd.concat([data, latest_df], ignore_index=True)
        updated_data = updated_data.drop_duplicates(subset=["날짜"]).reset_index(drop=True)
        updated_data.to_csv(CSV_FILE_PATH, index=False)
        print("CSV 파일이 성공적으로 업데이트되었습니다.")

        # 4. 머신러닝 모델 재학습
        print("머신러닝 모델 재학습 중...")
        X = updated_data[["번호1", "번호2", "번호3", "번호4", "번호5", "번호6"]]
        y = (updated_data["보너스"] > 20).astype(int)  # 보너스 번호가 20보다 큰 경우를 1로 설정
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        print("모델 학습 완료.")

        # 5. 모델 저장
        joblib.dump(model, MODEL_FILE_PATH)
        print(f"모델이 '{MODEL_FILE_PATH}' 경로에 저장되었습니다.")
    
    except Exception as e:
        print(f"업데이트 또는 재학습 중 오류 발생: {e}")