import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. 데이터 불러오기
data = pd.read_csv("로또봇.csv")  # CSV 파일이 같은 디렉토리에 위치한다고 가정

# 2. 입력 데이터(X)와 타겟 데이터(y) 생성
X = data[["번호1", "번호2", "번호3", "번호4", "번호5", "번호6"]]
y = (data["보너스"] > 20).astype(int)  # 예제: 보너스 번호가 20보다 큰 경우를 타겟으로 설정

# 3. 모델 생성 및 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. 모델 저장
joblib.dump(model, "ml_model.pkl")  # 모델을 파일로 저장
print("모델이 'ml_model.pkl'로 저장되었습니다.")