# -*- coding: utf-8 -*-
"""
name:
type:
cityID:
address:
lat:
lng:
url:
"""

import re
import os
import csv
import json
import time

import Geocode as gmap
    
regionList = ['[01]新北市', '[31]臺北市', '[32]臺北市', '[33]臺北市', '[34]臺北市', '[35]臺北市',
       '[36]臺北市', '[37]臺北市', '[38]臺北市', '[39]臺北市', '[40]臺北市', '[41]臺北市',
       '[42]臺北市']

path = './school/'
savepath='./school_data/'
filename = 'school_{}.json'

key = ''

for schooltype in os.listdir(path):
    filepath = path + schooltype
    with open(filepath, encoding='utf8') as rf:
        data = csv.DictReader(rf)
        for row in data:
            if row.get('縣市名稱') in regionList:
                temp = {}
                #name
                temp['name'] = row.get('學校名稱')
                #cityID & address
                address = row.get('地址')
                temp['cityID'] = re.findall(r'\[(\d{3})\]',address)[0]
                temp['address'] = address.split(']')[-1]
                #lat lng
                temp.update(gmap.geocoding(address, key))
                #type
                temp['type'] = 'school'
                #url
                temp['url'] = row.get('網址')

                print(row.get('代碼'))
                #save
                with open(savepath + filename.format(row.get('代碼')),
                         'w', encoding='utf8') as wf:
                    json.dump(temp, wf)
                time.sleep(0.05)
                
   
                