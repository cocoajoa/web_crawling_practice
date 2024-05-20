import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint


# url = 'https://new-m.pay.naver.com/savings/list/deposit?openLayer=true'
# headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }


# res = requests.get(url, headers=headers)
# soup = BeautifulSoup(res.text, 'html.parser')


## img 추출
# import os
# image_tags = soup.find_all('img')

# # 이미지를 다운로드할 디렉토리 생성
# os.makedirs('images', exist_ok=True)

# # 이미지를 순회하며 다운로드
# for img in image_tags:
#     img_url = img['src']
#     # 이미지 URL에서 http 또는 https로 시작하는 경우에만 처리
#     if img_url.startswith("http"):
#         # 이미지 다운로드
#         img_response = requests.get(img_url)
#         # 이미지 파일 저장
#         with open('images/{}'.format(os.path.basename(img_url)), 'wb') as f:
#             f.write(img_response.content)

### script 추출

# script_text = soup.find('script', attrs= { 'id': '__NEXT_DATA__' }).string

# data = json.loads(script_text)

# # # 스크립트 데이터에서 JSON 부분 추출

# # JSON 파싱
# # data = json.loads(script_text)

# # # companies 추출
# companies = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['result']['companies']

# # 결과 출력
# print(companies)


### 이미지 크롤링 후 저장 playwright로  클릭이나 호버시 나오는 페이지 긁기 가능

# import asyncio
# import os
# from playwright.async_api import async_playwright

# async def main():
#     async with async_playwright() as p:
#         # Chromium 브라우저를 시작
#         browser = await p.chromium.launch()
        
#         # 새 페이지 생성
#         page = await browser.new_page()
        
#         # 이미지를 다운로드할 웹 페이지 URL 설정
#         url = "https://new-m.pay.naver.com/savings/list/deposit?openLayer=true"
        
#         # 웹 페이지로 이동
#         await page.goto(url)
        
#         # 이미지 요소 선택자 설정
#         selector = ".CompanyGroupFilter_button-add-bank__zz_2d"
        
#         await page.click(selector)
        
#         await page.wait_for_load_state("networkidle")  # 비동기로하면 클릭 이전에 find_all이 돌아가네
        
#         content = await page.content()

#         # 이미지 URL 가져오기
#         image_urls = await page.query_selector_all('img')
#         image_urls = [await img.get_attribute("src") for img in image_urls]
        
#         # 이미지를 다운로드할 디렉토리 생성
#         os.makedirs('images', exist_ok=True)
        
#         # 이미지 다운로드
#         for index, image_url in enumerate(image_urls):
#             # 이미지 다운로드
#             image_content = requests.get(image_url).content
#             # 이미지 파일 저장
#             with open('images/{}.jpg'.format(index), 'wb') as f:
#                 f.write(image_content)
        
#         # 브라우저 세션 종료
#         await browser.close()

# # 비동기 함수 실행
# asyncio.run(main())
# print("이미지 다운로드 완료")

import asyncio
import os
from playwright.sync_api import sync_playwright

city_dict = {}

def what():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        url = 'https://www.kfcc.co.kr/map/main.do'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = browser.new_page()
        page.set_extra_http_headers(headers)        
        page.goto(url)
        for number in range(1, 17):
            page.evaluate(f'regionSet({number});')
            page.wait_for_selector('div#main_right')
            map_list_html = page.content()
            
            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(map_list_html, 'html.parser')
        
            # 해당 도시 확인 
            city_name = soup.select_one(f'a[href="javascript:regionSet({number});"]')
            
            # div#main_right 아래의 div.mapList 요소들을 추출
            map_list_elements = soup.select('div#main_right a')
            city_dict[city_name.string] = [element.string for element in map_list_elements]
            # 데이터 추출 및 city_name 리스트에 추가
            # for element in map_list_elements:
            #     print(element.string)
        
        browser.close()
from urllib.parse import urlencode
def that():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        params = {
            'r1':'서울',
            'r2':'마포구'
        }
        url = f'https://www.kfcc.co.kr/map/list.do?{urlencode(params)}'
        page = browser.new_page()
        page.set_extra_http_headers(headers)        
        page.goto(url)
   
        soup = BeautifulSoup(page.content(), 'html.parser')
        a_tags = soup.select('a.btn.small.blueBtn03')
        
        
        for a in a_tags:
            print(a.string)
     


        browser.close()

# what()
that()

