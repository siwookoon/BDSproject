import requests
import json
import jsonlines

service_key = '4d42486779706d3034365957634870'
data = []
for j in range(1,2):
  #url = f'http://openapi.seoul.go.kr:8088/{service_key}/json/tbLnOpendataRentV/{1+((j-1)*1000)}/{j*1000}'
  url = f'http://openapi.seoul.go.kr:8088/{service_key}/json/tbLnOpendataRentV/1/5/2023'
  print(url)
  req = requests.get(url)
  content = req.json()
  # print(content)
  con = content['tbLnOpendataRentV']['row']
  print(con)
  
  for h in con:
    dic = {}
    dic['SGG_CD'] = h['SGG_CD']
    dic['SGG_NM'] = h['SGG_NM']
    dic['BJDONG_CD'] = h['BJDONG_CD']
    dic['BJDONG_NM'] = h['BJDONG_NM']
    dic['BOBN'] = h['BOBN']
    dic['BUBN'] = h['BUBN']
    dic['FLR_NO'] = h['FLR_NO']
    dic['CNTRCT_DE'] = h['CNTRCT_DE']
    dic['RENT_GBN'] = h['RENT_GBN']
    dic['RENT_AREA'] = h['RENT_AREA']
    dic['RENT_GTN'] = h['RENT_GTN']
    dic['RENT_FEE'] = h['RENT_FEE']
    dic['BLDG_NM'] = h['BLDG_NM']
    dic['BUILD_YEAR'] = h['BUILD_YEAR']
    dic['HOUSE_GBN_NM'] = h['HOUSE_GBN_NM']
    data.append(dic)
print(data)
print('-' * 30)
print(data[0])
print('-' * 30)
print(data[1])
print('-' * 30)
print(data[2])
print('-' * 30)
print(dic)

answer = [{"prompt": "오늘의  가격은?", "completion": dic['BUILD_YEAR'] +'-'+ dic['SGG_NM']+'-'+ dic['BJDONG_CD']+'='+ dic['RENT_GTN']}]
with jsonlines.open('./chat.jsonl', 'w') as outfile:
    outfile.write_all(answer)
# with jsonlines.open('output.jsonl', 'w') as writer:
#     writer.write_all(items)content