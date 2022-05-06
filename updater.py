"""Update today prices."""

import csv
import datetime
from requests_html import HTMLSession

session = HTMLSession()

today = datetime.datetime.now().date()
todate = today.isoformat()

url = 'http://tank-ono.cz/cz/index.php?page=archiv'

data = {
  'txtDate': today.strftime("%d/%m/%Y"),
  'hod': "12",
  'min': "00"
}

r = session.post(url, data=data)

exclude = ['CZK', 'EUR']
item = [todate]
for x in r.html.find('table.cenik', first=True).find("td"):
    v = x.text.replace(',','.')
    if v == '.':
      v = ''
    if v not in exclude:
      item.append(v)

with open("prices.csv", "a") as f:
  csvw = csv.writer(f)
  csvw.writerow(item)