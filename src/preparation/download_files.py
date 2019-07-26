import requests
from bs4 import BeautifulSoup
import re
import zlib
import csv


url = "https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/"

# Get the names of all the csv files
with requests.Session() as s:
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    csvs = []
    for link in soup.find_all('a', attrs={'href': re.compile('^StormEvents')}):
        csvs.append(link.get('href'))

# Download
for c in csvs:
    res = requests.get(url + c)
    data = zlib.decompress(res.content, zlib.MAX_WBITS|32)
    if 'details' in c:
        folder = '/Users/jenny/Documents/storm-events/data/raw/details/'
    elif 'fatalities' in c:
        folder = '/Users/jenny/Documents/storm-events/data/raw/fatalities/'
    else:
        folder = '/Users/jenny/Documents/storm-events/data/raw/locations/'
    with open(folder + c[:-3], 'wb') as f:
        f.write(data)