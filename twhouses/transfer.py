# * -- codinf: utf-8 -- *
from os import listdir
import json
import time

import requests
from bs4 import BeautifulSoup


telList = ['#hd_mobile', '#hd_daytel' ,'#hd_nighttel']
def getDetail(url):
    detail={}
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    #set 'landlord'
    lord = []
    lord.append(soup.select_one('.ml5').text)
    for tel in telList:
        tmp = soup.select_one(tel)
        if tmp is not None:
            lord.append(tmp.get('value').replace('-',''))
    detail['landlord'] = ','.join(lord)

    #set title, floor, stories
    itemList = soup.select_one('ul.itemlist').select('li')
    detail['title'] = itemList[1].text
    for tempflr in itemList:
        if '整棟大樓樓層' in tempflr.text:
            flr = tempflr.text.split()
            detail['floor'] = flr[1].strip()
            detail['stories'] = flr[3].strip()
        elif '出租樓層' in tempflr.text:
            flr = tempflr.text.split()
            detail['floor'] = flr[1].strip()
            detail['stories'] = 'NA'
        else:
            detail['floor'] = 'NA'
            detail['stories'] = 'NA'
       

    #lat & lng
    if soup.select_one('#lng').get('value') is not None:
        detail['lng'] = float(soup.select_one('#lng').get('value'))
        detail['lat'] = float(soup.select_one('#lat').get('value'))
    else:
        detail['lng'] = 'NA'
        detail['lat'] = 'NA'

    #description
    detail['description'] = soup.select_one('#cont_note').text
    #Y?N
    yn_temp = soup.select_one('div.list')
    yn_temp = '' if yn_temp is None else yn_temp.text.split('\n')
    if '限女性' in yn_temp:
        detail['sex'] = 'F'
    elif '限男性' in yn_temp:
        detail['sex'] = 'M'
    else:
        detail['sex'] = 'A'
    detail['cook'] = 'Y' if '可開伙' in yn_temp else 'N'
    detail['pet'] = 'Y' if '可養寵物' in yn_temp else 'N'
    detail['smoke'] = 'Y' if '可抽煙' in yn_temp else 'N'
    detail['temp'] = 'Y' if '可短期租賃' in yn_temp else 'N'
    
    #special
    detail['patten'] = '水泥'
    

    return detail



if __name__=="__main__":
    inDir = './lowdata/'
    outFilePath = './data/{}.json'    

    for filename in listdir(inDir):
        with open(inDir + filename, encoding='utf-8') as rf:
            datas = json.loads(json.load(rf))
            
            for data in datas:
<<<<<<< HEAD
                try:
                    print(data['url'])
                    data.update(getDetail(data['url']))
                    twhouses_id = data.pop('twhouses_id')
                    data.pop('phone')
                    data['update']=data.pop('updateDate')
                    time.sleep(0.1)
                    with open(outFilePath.format(twhouses_id), 'w' ,encoding='utf-8') as wf:
                        json.dump(data, wf)
                except:
                    print('err')
=======
                time.sleep(1)
                try:
                    data.update(getDetail(data['url']))
                    twhouses_id = data.pop('twhouses_id')
                    data.pop('phone')
                    data['update']=data.pop('updataDate')
                    with open(outFilePath.format(twhouses_id), 'w' ,encoding='utf-8') as wf:
                        json.dump(data, wf)
                    time.sleep(1)
                except:
                    print('err')
>>>>>>> 173ebc8f1831dd4b4d878188185e638946c00650
