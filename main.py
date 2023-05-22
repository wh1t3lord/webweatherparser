import requests 
import csv
from datetime import datetime
from bs4 import BeautifulSoup

class parser:
 def __init__(self, url):
  self.url = url
  self.page = requests.get(url)
  now = datetime.now()
  current_time = now.strftime("%H-%M-%S")
  self.file_name = 'meteoinfo_' + current_time + '.csv'
  self.collected_data = []

  print(self.page)
  
class parserMeteoInfo(parser):
 def parse(self, list_cities, list_ids):
  for city in list_ids:
   new_url = self.build_request(city)
   response = requests.get(new_url)
   
   parsed_data = self.parse_requested_page(response)
   print(parsed_data)
   self.collected_data.append(parsed_data)

  self.save_to_csv(self.collected_data)

  
 def build_request(self, id_city, dt='0', has_db='1', dop='0'):
  result = ''
  
  result += self.url
  
  result += '?'

  result += ('id_city=' + id_city)

  return result
  
 def parse_requested_page(self, page):
  sp = BeautifulSoup(page.content, 'html.parser')
  rows = sp.find_all('tr')
  print(rows)
  result = []
  for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    result.append([ele for ele in cols if ele])



  return result

 def save_to_csv(self, parsed_data):
  with open(self.file_name, mode='w') as file:
   writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
   for city in parsed_data:
    analyzed = []

    for data in city:
     if len(data) < 2:
      continue
     else:
      analyzed.append(data[1])

    writer.writerow(analyzed)
 
def testMeteoInfo():
 prs = parserMeteoInfo('https://meteoinfo.ru/hmc-output/observ/obs_arch.php')
 
 csv = prs.parse(['Vladimir', 'Moscow'], ['1647', '1659'])
 
 
 

testMeteoInfo()