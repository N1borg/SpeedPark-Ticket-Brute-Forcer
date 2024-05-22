#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, random, time
from fake_useragent import UserAgent
from urllib.parse import urlencode
from bs4 import BeautifulSoup

ua = UserAgent()
random_user_agent = ua.random

url = 'https://www.kartingbowling.com/ce/index.php'
headers = {
    'User-Agent': random_user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.kartingbowling.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.kartingbowling.com/ce/index.php',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

data = {
    'code': '0000000000000',
    'btn': 'V%C3%A9rifier'
}

for n in range(6220000000000, 10**13, 10000):
    number = f'{n:013}'
    print(number)
    data['code'] = str(number)

    encoded_data = urlencode(data)

    response = requests.post(url, headers=headers, data=encoded_data)
    soup = BeautifulSoup(response.content, 'html.parser')
    p_rep = soup.find('p', class_='rep')
    if p_rep and f"Le ticket N°{data['code']} est périmé depuis" in p_rep.text:
        print("Number:" + data['code'] + "\n" + p_rep.text)
        break
    # else:
    #     print("No <p> tag with class 'rep' found.")

    time.sleep(random.uniform(0.2, 1.0))
