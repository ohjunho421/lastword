import requests
from bs4 import BeautifulSoup
from datetime import datetime

def crawl_latest_lotto():
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_sly.hst&fbm=0&acr=1&ie=utf8&query=로또당첨번호"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 당첨 번호 크롤링
    numbers = soup.select(".winning_number .ball")
    bonus = soup.select_one(".bonus_number .ball")

    if not numbers or not bonus:
        raise ValueError("크롤링 실패: 당첨 번호를 가져올 수 없습니다.")

    winning_numbers = [int(num.text) for num in numbers]  # 당첨 번호 추출
    bonus_number = int(bonus.text)  # 보너스 번호 추출

    # 현재 날짜 사용
    date = datetime.now().strftime("%Y-%m-%d")

    # 데이터 반환
    return {
        "날짜": date,
        "번호1": winning_numbers[0],
        "번호2": winning_numbers[1],
        "번호3": winning_numbers[2],
        "번호4": winning_numbers[3],
        "번호5": winning_numbers[4],
        "번호6": winning_numbers[5],
        "보너스": bonus_number,
    }