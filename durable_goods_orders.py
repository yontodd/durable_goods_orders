# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:09:45 2021

@author: jonat
"""

import requests
from datetime import datetime
import calendar
import pandas as pd
import numpy as np

current_report_month = ()

if datetime.now().month - 1 == 0:
  current_report_month = 12
else:
  current_report_month = datetime.now().month - 1

current_report_month = str(current_report_month).zfill(2)

current_report_year = ()

if current_report_month == 12:
  current_report_year = datetime.now().year -1
else:
  current_report_year = datetime.now().year

current_report_year = str(current_report_year)

current = current_report_year + "-" + current_report_month

previous_report_month = ()

if int(current_report_month) == 1:
  previous_report_month = 12
else:
  previous_report_month = int(current_report_month) - 1

previous_report_month = str(previous_report_month).zfill(2)

previous_report_year = ()

if current_report_month == 12:
  previous_report_year = int(current_report_year - 1)
else:
  previous_report_year = current_report_year

previous_report_year = str(previous_report_year)

previous = previous_report_year + "-" + previous_report_month

print("Current month: {}".format(current))
print("Prior month: {}".format(previous))

base_url = "https://api.census.gov/data/timeseries/eits/advm3?get=data_type_code,time_slot_id,seasonally_adj,category_code,cell_value,error_data&for=us:*&time=from+{}".format(previous)
response = requests.get(base_url)
data = response.json()
df = pd.DataFrame(data[1:], columns = data[0])

rpt_list = ["Headline durable goods orders", "Durable Goods (ex. transportation", "Core durable goods orders (ex. defense and aircraft)", "Core capital goods shipments (which feeds into GDP"]
data_type_code = ["MPCNO", "MPCNO", "MPCNO", "MPCVS"]
category_code = ["MDM", "DXT", "DXD", "NXA"]
cols = ["Report", "data_type_code","category_code"]
zip_list = pd.DataFrame(zip(rpt_list, data_type_code, category_code))
zip_list.columns = cols

type_variables = ["MPCNO","MPCVS"]
cat_variables = ["MDM","DXT","DXD","NXA"]
seas_code = "yes"
dg_data = df[(df.data_type_code.isin(type_variables)) &
   (df.category_code.isin(cat_variables)) &
   (df["seasonally_adj"] == seas_code)]

durable_goods_orders = pd.merge(zip_list, dg_data, how = 'left', left_on = ["data_type_code","category_code"], right_on = ["data_type_code","category_code"])

durable_goods_orders
