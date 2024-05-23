from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
# 크롤링으로 갖고 온 도시 정보, 없어지진 않을듯.. 아마
city_info = ['서울지역', '부산지역', '대구지역', '인천지역', '광주지역', '대전지역', '울산지역', '경기지역', '강원지역', '충북지역', '충남지역', '전북지역', '전남지역', '경북지역', '경남지역', '제주지역']
output_file_path = 'intr_info.json'
intr_info = {}
def processPage():
     with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            params = {
     
            }
            url = f'https://www.suhyup-bank.com/'
       
            page = browser.new_page()
            page.set_extra_http_headers(headers)        
            page.goto(url)
            page.wait_for_load_state('networkidle')
            
            page.set_default_timeout(5000)
            frame = page.frame(name='ib20_content_frame')
            if not frame:
                print("Frame not found")
            else:
                print('get')
                frame.hover('#gnbmenu > div > ul > li.menu04 > a')
                frame.click('#gnbmenu > div > ul > li.menu04 > div > ul > li:nth-child(4) > ul > li:nth-child(2) > a')
                frame.click('#COUNTRY_SELECT')
                
                # city_info = frame.eval_on_selector_all(
                #      '#COUNTRY_SELECT > option',
                #      'options => options.map(option => option.textContent.trim())'
                #      )

                # 도시 클릭
                for city_name in city_info:
                    # 지연 시간 대기
                    frame.wait_for_timeout(2000) 

                    # 도시 선택 및 클릭
                    frame.eval_on_selector(
                        f'#COUNTRY_SELECT > option:has-text("{city_name}")',
                        'option => option.click()'
                    )
       
        
                page.pause()
                

          
            # print(BeautifulSoup(page.content(), 'html.parser'))
            # frame_element = page.frame_locator('iframe[id="ib20_content_frame"][name="rateFrame2"]')
            # print(frame_element)
            # text = frame_element.locator('#gnbmenu > div > ul > li.menu04 > a').first
            # text.click()
            # print(text)
            # page.pause()
processPage()
# def process_page(city_name, city_district, j, page_no):
#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch()
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#             }
#             params = {
#                 'r1': city_name,
#                 'r2': city_district,
#                 'pageNo': page_no + 1
#             }
#             url = f'https://www.kfcc.co.kr/map/list.do?{urlencode(params)}'
#             print(city_name, city_district, j, page_no)
#             page = browser.new_page()
#             page.set_extra_http_headers(headers)        
#             page.goto(url)
#             page.wait_for_load_state('networkidle')
#             page.set_default_timeout(5000)
          

#             page.locator('a.btn.small.blueBtn03').nth(j).click()
#             page.wait_for_selector("#sub_tab_rate")

#             bank_name = page.query_selector('#div1 > div.pop-body.detail > div > div.top > div.title')
#             name = bank_name.inner_text()
#             element = page.query_selector('#sub_tab_rate')

#             if element:
#                 iframe_element = page.frame_locator('iframe[id="rateFrame"][name="rateFrame2"]')
#                 iframe_element.locator('a.tabw80').nth(1).click()

#                 # mg정기예금
#                 try:
#                     mg_fixed_rate = iframe_element.locator('table[summary="MG더뱅킹정기예금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr > td:nth-child(3)').text_content()
#                 except:
#                     mg_fixed_rate = '연0.0%'
#                 iframe_element.locator('a.tabw80').nth(2).click()

#                 # 정기적금
#                 try:
#                     mg_saving1_rate = iframe_element.locator('table[summary="정기적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(2) > td:nth-child(2)').first.text_content()
#                 except:
#                     mg_saving1_rate = '연0.0%'
#                 # mg정기적금
#                 try: 
#                     mg_saving2_rate = iframe_element.locator('table[summary="MG더뱅킹정기적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(2) > td:nth-child(2)').first.text_content()
#                 except:
#                     mg_saving2_rate = '연0.0%'
#                 # 자유적립적금
#                 try:
#                     mg_saving3_rate = iframe_element.locator('table[summary="자유적립적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(4) > td:nth-child(2)').first.text_content()
#                 except:
#                     mg_saving3_rate = '연0.0%'

#                 intr_info[name] = {
#                     '정기예금': mg_fixed_rate,
#                     '정기적금' : mg_saving1_rate,
#                     'mg정기적금' : mg_saving2_rate,
#                     '자유적립적금' : mg_saving3_rate
#                 }
#             button2 = page.query_selector('button.grayBtn')
#             button2.click()
#     except Exception as e:
#         print(f'Error processing page {j}: {e}')

# def find_intr(city_name, city_district, city_stores):
#     group_size = 10
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         futures = []
#         for i in range(0, city_stores, group_size):  # Assuming 100 as the maximum total_count
#             for j in range(i, i + group_size):
#                 index_page = j // group_size
#                 if index_page:
#                     futures.append(executor.submit(process_page, city_name, city_district, j, index_page))
#                 else:
#                     futures.append(executor.submit(process_page, city_name, city_district, j, 0))
                
#                 if j == city_stores - 1:
#                     break
 

# def getTotal(city_name, city_district):
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
        
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
#         params = {
#             'r1': city_name,
#             'r2': city_district,
#             'pageNo': 1
#         }
#         url = f'https://www.kfcc.co.kr/map/list.do?{urlencode(params)}'
#         page = browser.new_page()
#         page.set_extra_http_headers(headers)        
#         page.goto(url)
#         page.wait_for_load_state('networkidle')
#         page.set_default_timeout(5000)
#         total_count = page.locator('a.btn.small.blueBtn03').count()

#         return total_count

# find_intr(city, district, total_store)
      
        
# with open(output_file_path, 'w', encoding='utf-8') as json_file:
#     json.dump(intr_info, json_file, indent=4, ensure_ascii=False)

# print(f'Data saved to {output_file_path}')