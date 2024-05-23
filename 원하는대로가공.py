import json
from datetime import datetime

with open('intr_info.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Current datetime for updated_at
updated_at = datetime.now().strftime("%Y-%m-%d")

# Parse JSON data into Django fixtures format
fixtures = []
pk_counter = 1

for branch, accounts in data.items():
    bank_name = branch
    
    for account_type, rate in accounts.items():
        intr_rate = float(rate.replace("연", "").replace("%", ""))
        
        if "정기예금" == account_type:
            fixture = {
                "model": "bankDatas.FixedDeposit",
                "fields": {
                    "name": f'MG더뱅킹정기예금 ({bank_name})',
                    "updated_at": updated_at,
                    "join_member": "만 19세 이상의 실명의 개인",
                    "join_deny": '''공동명의예금으로 가입 불가, 
                                양도‧양수 및 계좌분할 불가''',
                    "join_way": "스마트뱅킹 “MG더뱅킹” 어플에서만 가입 가능", 
                    "save_trm" : 12,
                    "max_limit": 100000000,
                    "intr_rate": intr_rate,
                    "intr_rate2": intr_rate + 0.3,
                    "intr_rate_type": "",
                    "spcl_cnd": '''이 예금 가입일부터 만기일 전일까지 MG스마트알림서비스를 가입하고 1회 이상 로그인하는 경우
                                (단, MG스마트알림서비스에 기가입되어 있는 경우 이 예금 가입일부터 만기일 전일까지 1회 이상 로그인 하는 경우)
                                또는 이 예금 가입일부터 만기일 전일까지 MG더뱅킹 어플에서 더뱅킹PUSH알림서비스를 통해 1회 이상 입출금 PUSH알림을 받은 경우 : 연 0.1%
                                이 예금 가입시 만기자동이체를 등록한 경우 : 연 0.1%
                                이 예금 가입일부터 가입시 정한 만기일 전일까지 MG더뱅킹을 이용한 이체거래 실적이 6회 이상 있는 경우 : 연 0.1%''',
                    "etc_note": "(해지) 창구, 인터넷(스마트)뱅킹, 만기자동이체 신청 가능",
                    "bank_id": 102,
                    "pin_number" : 119112,
                    "bank_code": 119112,
                    "isCheck": True,
                    "views": 0
                }
            }
        elif "정기적금" == account_type:
            fixture = {
                "model": "bankDatas.SavingsAccount",
                "fields": {
                    "name": f'정기적금 ({bank_name})',
                    "updated_at": updated_at,
                    "join_member": "제한없음",
                    "join_deny": "제한없음",
                    "join_way": "지점별 상이", 
                    "save_trm" : 12,
                    "max_limit": 10000000000,
                    "intr_rate": intr_rate,
                    "intr_rate2": intr_rate,
                    "intr_rate_type": "단리",
                    "spcl_cnd": "",
                    "etc_note": "",
                    "rsrv_type_nm": "정액적립식",
                    "bank_id": 102,
                    "pin_number" : 119113,
                    "bank_code": 119112,
                    "isCheck": True,
                    "views": 0
                }
            }
        elif "mg정기적금" == account_type:
            fixture = {
                "model": "bankDatas.SavingsAccount",
                "fields": {
                    "name": f'MG더뱅킹정기적금 ({bank_name})',
                    "updated_at": updated_at,
                    "join_member": "만19세 이상의 실명의 개인 (금고별 1인 1계좌)",
                    "join_deny": "제한없음",
                    "join_way": "(가입) 스마트뱅킹 “MG더뱅킹” 어플에서만 가입 가능", 
                    "save_trm" : 12,
                    "max_limit": 1000000,
                    "intr_rate": intr_rate,
                    "intr_rate2": intr_rate + 0.5,
                    "intr_rate_type": "단리",
                    "spcl_cnd": '''최고 연 0.5% (모든 우대이율은 만기해지하는 경우에만 적용)

이 예금 가입일부터 만기일 전일까지 MG스마트알림서비스를 가입하고 1회 이상 로그인하는 경우
(단, MG스마트알림서비스에 기가입되어 있는 경우 이 예금 가입일부터 만기일 전일까지 1회 이상 로그인 하는 경우)
또는 이 예금 가입일부터 만기일 전일까지 MG더뱅킹 어플에서 더뱅킹PUSH알림서비스를 통해 1회 이상 입출금 PUSH알림을 받은 경우 : 연 0.2%
이 예금 가입시 만기자동이체를 등록한 경우 : 연 0.1%

새마을금고 요구불예금에서 이 예금 자동이체 시 : 연 0.1%

※ 계약기간 6개월은 3회 이상, 1년은 6회 이상 자동이체로 납입하는 경우

이 예금 가입일로부터 1개월내 이 예금 개설금고 거치식 상품을 추가로 가입하고 해당 상품을 만기해지하거나 이 예금 만기일 현재까지 유지한 경우 : 연 0.1%
                            ''',
                    "etc_note": "(해지) 창구, 인터넷(스마트)뱅킹, 만기자동이체 신청 가능",
                    "rsrv_type_nm": "정액적립식",
                    "bank_id": 102,
                    "pin_number" : 119114,
                    "bank_code": 119112,
                    "isCheck": True,
                    "views": 0
                }
            }
        elif "자유적립적금" == account_type:
            fixture = {
                "model": "bankDatas.SavingsAccount",
                "fields": {
                    "name": f'MG월복리자유적금 ({bank_name})',
                    "updated_at": updated_at,
                    "join_member": "실명에 의한 개인(1인 1계좌)",
                    "join_deny": "실명에 의한 개인(1인 1계좌)",
                    "join_way": "지점별 상이", 
                    "save_trm" : 12,
                    "max_limit": 30000000,
                    "intr_rate": intr_rate,
                    "intr_rate2": intr_rate + 0.7,
                    "intr_rate_type": "복리",
                    "spcl_cnd": '''아래의 우대이율 요건을 충족할 경우 최대 연 0.7%까지 우대이율 지급 다만, 5호의 우대이율의 한도는 0.1% 지급
① 가입일 당시 화수분 또는 화수분II예금 가입자 연 0.1%
② 가입일 기준 3개월 이내에 신규가입 회원 연 0.1%
③ 가입일전 1개월이내 거치식예금을 가입하여 유지하고 있는자 연 0.2%
④ 가입일전 1개월이내 적립식예금을 가입하여 유지하고 있는자 연 0.1%
⑤ 계약기간 내 본인을 포함한 세대구성원 2인 이상이 가입시 연 0.1%
⑥ 가입일 전월말 기준 직전 3개월간 입출금이 자유로운 예금 평잔이 30만원 이상인 경우 연 0.1%
''',
                    "etc_note": "",
                    "rsrv_type_nm": "자유적립식",
                    "bank_id": 102,
                    "pin_number" : 119115,
                    "bank_code": 119112,
                    "isCheck": True,
                    "views": 0
                }
            }
        
        fixtures.append(fixture)
        

# Convert fixtures to JSON
fixtures_json = json.dumps(fixtures, ensure_ascii=False, indent=4)

# Save to a file
with open('newtown.json', 'w', encoding='utf-8') as f:
    f.write(fixtures_json)

print(fixtures_json)