# -*- coding: utf-8 -*-

import requests
import datetime
import pandas as pd
import numpy as np

current_year = '2021'
current_month = '03'
current = current_year + "-" + current_month

prior_month = ()
prior_year = ()

if current_month == 1:
  prior_month = 12
else:
  prior_month = str((int(current_month) - 1)).zfill(2)

if current_month == 1:
  prior_year = str((int(current_year) - 1))
else:
  prior_year = (current_year)

prior = prior_year + '-' + prior_month

print("Current month: {}".format(current))
print("Prior month: {}".format(prior))

base_url = "https://api.census.gov/data/timeseries/eits/advm3?get=data_type_code,time_slot_id,seasonally_adj,category_code,cell_value,error_data&for=us:*&time=from+{}".format(prior)

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

