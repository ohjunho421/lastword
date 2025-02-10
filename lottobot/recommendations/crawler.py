import requests
from bs4 import BeautifulSoup
from .models import LottoData

def fetch_latest_lotto_data():
    url = "https://search.naver.com/search.naver?query=로또당첨번호"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    winning_number_div = soup.find("div", class_="winning_number")
    winning_numbers = [int(span.text) for span in winning_number_div.find_all("span", class_="ball")]

    bonus_number_div = soup.find("div", class_="bonus_number")
    bonus_number = int(bonus_number_div.find("span", class_="ball").text)

    draw_number = LottoData.objects.count() + 1  # 회차 번호 추정

    return {
        "draw_number": draw_number,
        "winning_numbers": winning_numbers,
        "bonus_number": bonus_number,
    }