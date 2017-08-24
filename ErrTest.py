# -*- coding: utf-8 -*-

import os
import json

def getErr(path='./'):
    errList = []
    for name in os.listdir(path):
        with open(path + name , 'r', encoding='utf8') as f:
            data = json.load(f)
            if data.get('status'):
                errList.append(name)
    return errList
