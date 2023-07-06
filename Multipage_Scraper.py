# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 19:31:03 2023

@author: Justin
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
from random import randint
from time import sleep
cwd = os.getcwd()
  
URL = 'https://www.osha.gov/ords/imis/establishment.search?establishment=Construction&state=all&officetype=all&office=all&sitezip=100000&startmonth=07&startday=05&startyear=2018&endmonth=07&endday=05&endyear=2023&p_case=all&p_violations_exist=both&p_start=&p_finish=0&p_sort=12&p_desc=DESC&p_direction=Next&p_show=20'
  
req = requests.get(URL)
soup = bs(req.text, 'html.parser')
  
tables = soup.findChildren('table')

key_table = tables[1]
table_headers = key_table.findChildren('th')
table_content = key_table.findChildren('tr')

header_list = [i.text for i in table_headers]

df_row_list = []

for counter in range(0,30001,10000):
    temp_URL = 'https://www.osha.gov/ords/imis/establishment.search?establishment=Construction&state=all&officetype=all&office=all&sitezip=100000&startmonth=07&startday=05&startyear=2018&endmonth=07&endday=05&endyear=2023&p_case=all&p_violations_exist=both&p_start=&p_finish=' + str(counter) + '&p_sort=12&p_desc=DESC&p_direction=Next&p_show=10000'
    
    temp_req = requests.get(temp_URL)
    temp_soup = bs(temp_req.text, 'html.parser')
      
    temp_tables = temp_soup.findChildren('table')

    key_table = temp_tables[1]
    table_headers = key_table.findChildren('th')
    table_content = key_table.findChildren('tr')
    
    print('Working thru page...')
    
    for row in range(1,len(table_content)):    
        one_row = [i.text for i in table_content[row] if i.text != '\n']
        df_row_list.append(one_row)
    
    sleep(randint(2,10))
    
df = pd.DataFrame(df_row_list, columns = header_list)

df.to_csv(cwd + '/OSHA Construction Data.csv')

print('Done running')