from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import CityName
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from asgiref.sync import sync_to_async

@sync_to_async
def crawl_website():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # 헤더 추가
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page.set_extra_http_headers(headers)

        page.goto('https://www.kfcc.co.kr/map/main.do')

        # 버튼 클릭r
        for number in range(1, 17):
            page.evaluate(f'regionSet({number});')

            # 버튼을 클릭한 후 나타나는 동적인 요소에 대한 처리
            dynamic_element = page.wait_for_selector('div#main_right')
            li_elements = dynamic_element.query_selector_all('li')

            # 데이터 추출 및 저장
            for li_element in li_elements:
                li_text = li_element.inner_text()
                print(li_text)
                CityName.objects.create(title=li_text)

        browser.close()

async def search(request):
    await crawl_website()
    return render(request, 'index.html')
