
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
from datetime import datetime

# 한글은 장고 DB 모델 이름 
# 도시 구역별 페이지 수 확인, 10개 당 1 페이지임
def getTotal(city_name, city_district):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        params = {
            'r1': city_name,
            'r2': city_district,
            'pageNo': 1
        }
        url = f'https://www.kfcc.co.kr/map/list.do?{urlencode(params)}'
        page = browser.new_page()
        page.set_extra_http_headers(headers)        
        page.goto(url)
        page.wait_for_load_state('networkidle')
        page.set_default_timeout(5000)
        total_count = page.locator('a.btn.small.blueBtn03').count()

        return total_count

# Current datetime for updated_at
updated_at = datetime.now().strftime("%Y-%m-%d")
# 받은 정보들을 통해 지점별 상품들 확인 후 DB 비교
def process_page(city_name, city_district, j, page_no):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            params = {
                'r1': city_name,
                'r2': city_district,
                'pageNo': page_no + 1
            }
            url = f'https://www.kfcc.co.kr/map/list.do?{urlencode(params)}'
            print(city_name, city_district, j, page_no)
            page = browser.new_page()
            page.set_extra_http_headers(headers)        
            page.goto(url)
            page.wait_for_load_state('networkidle')
            page.set_default_timeout(5000)
          

            page.locator('a.btn.small.blueBtn03').nth(j).click()
            page.wait_for_selector("#sub_tab_rate")

            bank_name = page.query_selector('#div1 > div.pop-body.detail > div > div.top > div.title')
            name = bank_name.inner_text()
            element = page.query_selector('#sub_tab_rate')
            
            if element:
                iframe_element = page.frame_locator('iframe[id="rateFrame"][name="rateFrame2"]')
                iframe_element.locator('a.tabw80').nth(1).click()

                # mg정기예금
                try:
                    mg_fixed_rate = iframe_element.locator('table[summary="MG더뱅킹정기예금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr > td:nth-child(3)').text_content()
                    mg_fixed_name = f'MG더뱅킹정기예금 ({name})'
                except:
                    mg_fixed_rate = '연0.0%'
                iframe_element.locator('a.tabw80').nth(2).click()

                # 정기적금
                try:
                    mg_saving1_rate = iframe_element.locator('table[summary="정기적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(2) > td:nth-child(2)').first.text_content()
                    mg_saving1_name = f'정기적금 ({name})'
                except:
                    mg_saving1_rate = '연0.0%'
                # mg정기적금
                try: 
                    mg_saving2_rate = iframe_element.locator('table[summary="MG더뱅킹정기적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(2) > td:nth-child(2)').first.text_content()
                    mg_saving2_name = f'MG더뱅킹정기적금 ({bank_name})'
                except:
                    mg_saving2_rate = '연0.0%'
                # 자유적립적금
                try:
                    mg_saving3_rate = iframe_element.locator('table[summary="자유적립적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(4) > td:nth-child(2)').first.text_content()
                    mg_saving3_name = f'MG월복리자유적금 ({bank_name})'
                except:
                    mg_saving3_rate = '연0.0%'
                ####### 상품들 이율 확인 완료 ######
                    
                # 상품이 없으면 이율 없음
                if mg_fixed_name:
                    if 정기예금.objects.filter(name = mg_fixed_name).exists(): 
                        existing_instance = 정기예금.objects.get(name = mg_fixed_name)
                        new_intr_rate = mg_fixed_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate + 0.3
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = 정기예금DB(
                        name = mg_fixed_name,
                        updated_at = updated_at,
                        join_member = '만 19세 이상의 실명의 개인',
                        join_deny = '''공동명의예금으로 가입 불가, 
                                양도‧양수 및 계좌분할 불가''',
                        join_way = '스마트뱅킹 “MG더뱅킹” 어플에서만 가입 가능',
                        save_trm = 12,
                        max_limit = 100000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate + 0.3,
                        intr_rate_type  = '',
                        spcl_cnd = '''이 예금 가입일부터 만기일 전일까지 MG스마트알림서비스를 가입하고 1회 이상 로그인하는 경우
                                (단, MG스마트알림서비스에 기가입되어 있는 경우 이 예금 가입일부터 만기일 전일까지 1회 이상 로그인 하는 경우)
                                또는 이 예금 가입일부터 만기일 전일까지 MG더뱅킹 어플에서 더뱅킹PUSH알림서비스를 통해 1회 이상 입출금 PUSH알림을 받은 경우 : 연 0.1%
                                이 예금 가입시 만기자동이체를 등록한 경우 : 연 0.1%
                                이 예금 가입일부터 가입시 정한 만기일 전일까지 MG더뱅킹을 이용한 이체거래 실적이 6회 이상 있는 경우 : 연 0.1%''',
                        etc_note = '(해지) 창구, 인터넷(스마트)뱅킹, 만기자동이체 신청 가능',
                        bank_id = 102,
                        pin_number = 119112,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if 정기예금.objects.filter(name = mg_fixed_name).exists():
                        existing_instance = 정기예금.objects.get(name = mg_fixed_name)
                        existing_instance.delete()
                
                if mg_saving1_name:
                    if 적금.objects.filter(name = mg_saving1_name).exists():
                        existing_instance = 적금.objects.get(name = mg_saving1_name)
                        new_intr_rate = mg_saving1_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = 적금(
                        name = mg_saving1_name,
                        updated_at = updated_at,
                        join_member = '제한없음',
                        join_deny = '제한없음',
                        join_way = '지점별 상이',
                        save_trm = 12,
                        max_limit = 100000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate,
                        intr_rate_type  = "단리",
                        spcl_cnd = '',
                        etc_note = '',
                        rsrv_type = '정액적립식',
                        bank_id = 102,
                        pin_number = 119113,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if 적금.objects.filter(name = mg_saving1_name).exists():
                        existing_instance = 적금.objects.get(name = mg_saving1_name)
                        existing_instance.delete()
                
                
                if mg_saving2_name:
                    if 적금.objects.filter(name = mg_saving2_name).exists():
                        existing_instance = 적금.objects.get(name = mg_saving2_name)
                        new_intr_rate = mg_saving2_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate + 0.5
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = 적금(
                        name = mg_saving2_name,
                        updated_at = updated_at,
                        join_member = '만19세 이상의 실명의 개인 (금고별 1인 1계좌)',
                        join_deny = '제한없음',
                        join_way = '(가입) 스마트뱅킹 “MG더뱅킹” 어플에서만 가입 가능',
                        save_trm = 12,
                        max_limit = 1000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate + 0.5,
                        intr_rate_type  = "단리",
                        spcl_cnd = '''최고 연 0.5% (모든 우대이율은 만기해지하는 경우에만 적용)

이 예금 가입일부터 만기일 전일까지 MG스마트알림서비스를 가입하고 1회 이상 로그인하는 경우
(단, MG스마트알림서비스에 기가입되어 있는 경우 이 예금 가입일부터 만기일 전일까지 1회 이상 로그인 하는 경우)
또는 이 예금 가입일부터 만기일 전일까지 MG더뱅킹 어플에서 더뱅킹PUSH알림서비스를 통해 1회 이상 입출금 PUSH알림을 받은 경우 : 연 0.2%
이 예금 가입시 만기자동이체를 등록한 경우 : 연 0.1%

새마을금고 요구불예금에서 이 예금 자동이체 시 : 연 0.1%

※ 계약기간 6개월은 3회 이상, 1년은 6회 이상 자동이체로 납입하는 경우

이 예금 가입일로부터 1개월내 이 예금 개설금고 거치식 상품을 추가로 가입하고 해당 상품을 만기해지하거나 이 예금 만기일 현재까지 유지한 경우 : 연 0.1%
                            ''',
                        etc_note = '(해지) 창구, 인터넷(스마트)뱅킹, 만기자동이체 신청 가능',
                        rsrv_type = '정액적립식',
                        bank_id = 102,
                        pin_number = 119114,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if 적금.objects.filter(name = mg_saving2_name).exists():
                        existing_instance = 적금.objects.get(name = mg_saving2_name)
                        existing_instance.delete()
                if mg_saving3_name:
                    if 적금.objects.filter(name = mg_saving3_name).exists():
                        existing_instance = 적금.objects.get(name = mg_saving3_name)
                        new_intr_rate = mg_saving3_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate + 0.7
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = 적금DB(
                        name = mg_saving3_name,
                        updated_at = updated_at,
                        join_member = '실명에 의한 개인(1인 1계좌)',
                        join_deny = '실명에 의한 개인(1인 1계좌)',
                        join_way = '지점별 상이',
                        save_trm = 12,
                        max_limit = 30000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate + 0.7,
                        intr_rate_type  = "복리",
                        spcl_cnd = '''아래의 우대이율 요건을 충족할 경우 최대 연 0.7%까지 우대이율 지급 다만, 5호의 우대이율의 한도는 0.1% 지급
① 가입일 당시 화수분 또는 화수분II예금 가입자 연 0.1%
② 가입일 기준 3개월 이내에 신규가입 회원 연 0.1%
③ 가입일전 1개월이내 거치식예금을 가입하여 유지하고 있는자 연 0.2%
④ 가입일전 1개월이내 적립식예금을 가입하여 유지하고 있는자 연 0.1%
⑤ 계약기간 내 본인을 포함한 세대구성원 2인 이상이 가입시 연 0.1%
⑥ 가입일 전월말 기준 직전 3개월간 입출금이 자유로운 예금 평잔이 30만원 이상인 경우 연 0.1%
''',
                        etc_note = '',
                        rsrv_type = '자유적립식',
                        bank_id = 102,
                        pin_number = 119115,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if 적금.objects.filter(name = mg_saving3_name).exists():
                        existing_instance = 적금.objects.get(name = mg_saving3_name)
                        existing_instance.delete()
                
            button2 = page.query_selector('button.grayBtn')
            button2.click()
    except Exception as e:
        print(f'Error processing page {j}: {e}')



# 크롤링을 하는데 비동기식으로 도시 구역별 페이지 돌림
def find_intr(city_name, city_district, city_stores):
    group_size = 10
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for i in range(0, city_stores, group_size):  # Assuming 100 as the maximum total_count
            for j in range(i, i + group_size):
                index_page = j // group_size
                if index_page:
                    futures.append(executor.submit(process_page, city_name, city_district, j, index_page))
                else:
                    futures.append(executor.submit(process_page, city_name, city_district, j, 0))
                
                if j == city_stores - 1:
                    break
 
city_info = {
    '인천': ['강화군', '서구', '동구', '중구', '미추홀구', '연수구', '계양구', '부평구', '남동구', '옹진군'], 
    '서울': ['도봉구', '마포구', '관악구', '강북구', '용산구', '서초구', '노원구', '성동구', '강남구', '성북구', '광진구', '송파구', '은평구', 
           '강서구', '강동구', '종로구', '양천구', '중랑구', '영등포구', '서대문구', '구로구', '동대문구', '동작구', '중구', '금천구'], 
    '강원': ['철원군', '화천군', '양구군', '춘천시', '인제군', '고성군', '속초시', '양양군', '홍천군', '강릉시', '원주시', '횡성군', '평창군', '영월군', '정선군', '동해시', '삼척시', '태백시'], 
    '경기': ['김포시', '파주시', '연천군', '고양시', '양주시', '동두천시', '포천시', '의정부시', '남양주시', '구리시', '가평군', '하남시', '부천시', '광명시', '시흥시', '안산시', '안양시', 
           '과천시', '군포시', '의왕시', '성남시', '광주시', '양평군', '화성시', '수원시', '오산시', '용인시', '이천시', '여주시', '평택시', '안성시'], 
    '충북': ['청주시', '진천군', '음성군', '충주시', '제천시', '괴산군', '단양군', '보은군', '옥천군', '영동군', '증평군'], 
    '충남': ['태안군', '서산시', '당진시', '홍성군', '예산군', '아산시', '천안시', '보령시', '청양군', '공주시', '서천군', '부여군', '논산시', '금산군', '계룡시'], 
    '대전': ['유성구', '대덕구', '서구', '중구', '동구'], 
    '경북': ['문경시', '예천군', '영주시', '봉화군', '울진군', '상주시', '의성군', '안동시', '영양군', '김천시', '구미시', '청송군', '영덕군', '성주군', '칠곡군', 
           '영천시', '포항시', '고령군', '경산시', '경주시', '청도군', '울릉군'], 
    '대구': ['서구', '북구', '동구', '달서구', '중구', '남구', '수성구', '달성군', '군위군'], 
    '전북': ['군산시', '익산시', '부안군', '김제시', '완주군', '전주시', '고창군', '정읍시', '순창군', '임실군', '진안군', '무주군', '남원시', '장수군'], 
    '울산': ['울주군', '북구', '중구', '남구', '동구'], 
    '광주': ['광산구', '북구', '서구', '남구', '동구'], 
    '경남': ['함양군', '거창군', '산청군', '합천군', '하동군', '진주시', '의령군', '함안군', '창녕군', '남해군', '사천시', '고성군', '창원시', '밀양시', '통영시', '거제시', '김해시', '양산시'], 
    '부산': ['강서구', '북구', '금정구', '기장군', '사상구', '부산진구', '연제구', '동래구', '사하구', '서구', '중구', '동구', '남구', '수영구', '해운대구', '영도구'], 
    '전남': ['영광군', '장성군', '담양군', '함평군', '신안군', '무안군', '나주시', '화순군', '곡성군', '구례군', '목포시', 
           '영암군', '진도군', '해남군', '강진군', '장흥군', '보성군', '순천시', '완도군', '고흥군', '여수시', '광양시'], 
    '제주': ['제주시', '서귀포시'],
    '세종': ['세종시']
}

# 도시별, 지점별 총 페이지 수를 구하고 정기예금, 적금 상품들을 크롤링하여 기존 DB와 비교하여 업데이트한다.
for city in city_info:
    for district in city_info[city]:
        total_store = getTotal(city, district)
        find_intr(city, district, total_store)
      


# isCheck가 false인건 DB에서 지울 것