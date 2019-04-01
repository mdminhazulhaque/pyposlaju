#!/usr/bin/env python3

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

"""
Copyright (c) 2018 Md. Minhazul Haque
This file is part of mdminhazulhaque/bd-mrp-api
(see https://github.com/mdminhazulhaque/banglalionwimaxapi).
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

import requests
import re
import tabulate

def truncate(data, limit=50):
    return data[:limit] + '..' * (len(data) > limit)

def poslaju_info(trackingno):
    _data = {
        'trackingNo03': trackingno
    }
    
    response = requests.post('https://www.pos.com.my/postal-services/quick-access/?track-trace', data=_data).text
    regex = re.compile(r'var strTD =  "(.*?)</table>";', re.S|re.M)
    table = regex.search(response).group(1)
    
    soup = BeautifulSoup(table, "lxml")
    rows = soup.find_all("table")[1].find_all("tr")
    
    data = []
    for row in rows:
        cells = row.find_all("td")
        items = []
        for cell in cells:
            items.append(PosLaju.truncate(cell.text.strip()))
        data.append(items)
    data.pop(0) # first row has headers
    
    print(tabulate.tabulate(data, headers=["datetime", "details", "location"], tablefmt="simple"))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Pos Laju Tracking Info Checker", add_help=False)
    parser.add_argument('-t', dest='trackingno', action="store", required=True, type=str)
    args = parser.parse_args()
    
    try:
        poslaju_info(args.trackingno)
    except Exception as r:
        print(r)
    
