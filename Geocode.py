# -*- coding: utf-8 -*-

import requests
import time
import re
import json

apiurl = 'https://maps.googleapis.com/maps/api/geocode/json'


def geocoding(address, key = ''):
    queryData = {}
    queryData['address'] = address
    queryData['key'] = ''
    res = requests.get(apiurl, params=queryData)
    code = res.json()
    time.sleep(0.02)
    res.close()
    if code.get('status') == 'OK':
        result = {}
        for add_comp in code['results'][0]['address_components']:
            if 'postal_code' in add_comp['types']:
                result['cityID'] = add_comp.get('long_name')
        result.update(code['results'][0]['geometry']['location'])
        return result
    else:
        return {'status':code.get('status')}
    


# def pregeocoding(latlng, key=''):
#     queryData = {}
#     queryData['latlng'] = latlng
#     queryData['key'] = key
#     queryData['language'] = 'zh-TW'
#     ress = requests.get(apiurl, params=queryData)
#     geo = ress.json()
#     res.close()
#     if geo.get('status') == 'OK':       
#         formatted_address=list(map( lambda x : x.get('formatted_address') , geo['results']))
#         address_list = list(filter( lambda x : re.match(r'^\d+.*[號]',x), formatted_address))
#         if len(address_list) > 0:
#             return {'address':address_list[0]}
#         else:
#             return {'address':max(formatted_address, key=len)}
#     else:
#         return {'status':geo.get('status')}
#     time.sleep(0.02)


def getID(address):
    region_id = {
    "中正區":100,
    "大同區":103,
    "中山區":104,
    "松山區":105,
    "大安區":106,
    "萬華區":108,
    "信義區":110,
    "士林區":111,
    "北投區":112,
    "內湖區":114,
    "南港區":115,
    "文山區":116,
    "萬里區":207,
    "金山區":208,
    "板橋區":220,
    "汐止區":221,
    "深坑區":222,
    "石碇區":223,
    "瑞芳區":224,
    "平溪區":226,
    "雙溪區":227,
    "貢寮區":228,
    "新店區":231,
    "坪林區":232,
    "烏來區":233,
    "永和區":234,
    "中和區":235,
    "土城區":236,
    "三峽區":237,
    "樹林區":238,
    "鶯歌區":239,
    "三重區":241,
    "新莊區":242,
    "泰山區":243,
    "林口區":244,
    "蘆洲區":247,
    "五股區":248,
    "八里區":249,
    "淡水區":251,
    "三芝區":252,
    "石門區":253}
    try:
        tmp = re.findall(r'..區', address)[0]
        return region_id.get(tmp)
    except:
        return None

def save_as_json(data = {}, filepath='./temp.json'):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data,f)
    except:
        print('err')