# –– coding: utf-8 ––
import json
import datetime
import re

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def getTotalPages(request):
    soup = BeautifulSoup(request.text, 'lxml')
    return int(soup.select('div > span')[-1].text)

def rent2n(rent_str):
    temp = ''.join(rent_str.split('/')[0].strip().split(','))
    return temp if isinstance(temp, int) else "NA"

def space2n(space_str):
    temp = space_str.split('/')[0].strip()
    return temp if isinstance(temp, float) else "NA"

def updateDate(Zhdate):
    day = re.match('(\d*)', Zhdate).group(1)
    if day == '':
        return datetime.date.today().strftime('%Y-%m-%d')
    else:
        try:
            day = int(day)
            return (datetime.date.today() - datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        except Exception:
            pass

def product(*seqs):
    if not seqs:
        return [[]]
    else:
        return [[x] + p for x in seqs[0] for p in product(*seqs[1:])]

def transfer(df):
    #remove header
    df = df.drop(0)
    #remove NaN
    df = df.dropna(axis=1)
    # setting fields name
    df.columns = ['twhouses_id',
                  'cityID',
                  'address',
                  'space',
                  'label',
                  'rent',
                  'phone',
                  'updateDate'
                 ]
    # make 'url'
    df['url'] = 'http://detail.twhouses.com.tw/House/Rent/' + df['twhouses_id']
    # paser 'rent' to integer
    df['rent'] = df['rent'].apply(rent2n)
    # 'space' is float
    df['space'] = df['space'].apply(space2n)
    # append address
    import re
    df['address'] = df['cityID'].apply(lambda x : re.sub('\[|\]','',x))\
                    + df['address'].apply(lambda x : x.split()[0])
    # update Date
    df['updateDate'] = df['updateDate'].apply(updateDate)
    # lebel
    df['label'] = df['label'].apply(lambda x: x[0])
    # region id
    df['cityID'] = df['cityID'].apply(getID)
    return df


def getID(region):
    region_id = {"台北市":{
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
        "文山區":116},
        "新北市":{
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
        "石門區":253,}}
    tmp = re.sub('\W',' ',region).split()
    return region_id.get(tmp[0]).get(tmp[1])


if __name__=="__main__":
    uri = 'http://116.50.40.135/phptwhouses/searchresultcontent.php'
    query_data = {'jsoncallback': 'jsonp1502695203491',
             '_': '1502704801831', 
             'region_id': '新北市', 
             'tradetype': '1', 
             'usingtype': '12', 
             'pageindex': '1', 'showtype': '1'
             }

    regionList = ['新北市','台北市']
    usingtypeList = [11,12,13] #住宅,套房,雅房 resp

    for query in product(regionList , usingtypeList):
        query_data['region_id'] = query[0]
        query_data['usingtype'] = query[1]
        res = requests.get(uri,query_data)
        totalPages = getTotalPages(res)
        url = res.url.replace('pageindex=1','pageindex={}')

        for pageindex in range(1,totalPages+1):
            df = pd.read_html(url.format(pageindex))[0]
            print(transfer(df))
    