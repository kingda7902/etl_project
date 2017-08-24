# -*- coding: utf-8 -*-

import requests
import time

apiurl = 'https://maps.googleapis.com/maps/api/geocode/json'
queryData = {'address':'', 'key':''}

def geocoding(address, key):
    queryData['address'] = address
    queryData['key'] = key
    res = requests.get(apiurl, params=queryData)
    code = res.json()
    if code.get('status') == 'OK':
        result = {}
        for add_comp in code['results'][0]['address_components']:
            if 'postal_code' in add_comp['types']:
                result['cityID'] = add_comp.get('long_name')
        result.update(code['results'][0]['geometry']['location'])
        return result
    else:
        return {'status':code.get('status')}
    time.sleep(0.02)