# –– coding: utf-8 ––
import json

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


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






