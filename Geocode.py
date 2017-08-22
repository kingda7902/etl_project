# -*- coding: utf-8 -*-

import requests


apiurl = 'https://maps.googleapis.com/maps/api/geocode/json'
queryData = {'address':'', 'key':''}

def geocoding(address, key):
    queryData['address'] = address
    queryData['key'] = key
    res = requests.get(apiurl, params=queryData)
    code = res.json()
    if code.get('status') == 'OK':
        return code['results'][0]['geometry']['location']
    else:
        return {'status':code.get('status')}