"""Scrape all the historical prices."""

import datetime
from requests_html import HTMLSession
import pandas as pd
# import time

session = HTMLSession()

url = 'http://tank-ono.cz/cz/index.php?page=archiv'

start_date = '2022-05-06'
end_date = '2012-01-01' # first date with available prices

data={
  'txtDate': '02/05/2022',
  'hod': "12",
  'min': "00"
}


results = []
exclude = ['CZK', 'EUR']
current_date = start_date
i = 0
while current_date >= end_date:
  current_day = datetime.date.fromisoformat(current_date)
  data['txtDate'] = current_day.strftime("%d/%m/%Y")
  r = session.post(url, data=data)
  item = [current_date]
  for x in r.html.find('table.cenik', first=True).find("td"):
    v = x.text.replace(',','.')
    if v == '.':
      v = ''
    if v not in exclude:
      item.append(v)
  results.append(item)
  current_date = (current_day + datetime.timedelta(-1)).isoformat()
  i += 1
  if (i % 100) == 0:
    print(current_date)

header0 = ['91', '95', '98', 'E85', 'D', 'EKOD', 'D+', 'AdB', 'LPG', 'w', 'W']
pre = ['CZK', 'EUR']
header = ['date']
for p in pre:
  for h in header0:
    header.append(p + '_' + h)

df = pd.DataFrame(results, columns=header)
df.to_csv('prices.csv', index=False)
