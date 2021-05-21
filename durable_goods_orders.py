# -*- coding: utf-8 -*-

# Estimates:

headline_est = 2.5
durable_ex_trans_est = 1.5

"""# Code - to pull key Durable Goods Orders indicators"""

import requests
import pandas as pd
import numpy as np
import datetime

base_url = "https://api.census.gov/data/timeseries/eits/advm3?get=data_type_code,time_slot_id,seasonally_adj,category_code,cell_value,error_data&for=us:*&time=from+{}".format("2020-03")
response = requests.get(base_url)
data = response.json()
df = pd.DataFrame(data[1:], columns = data[0])

df["time"] = pd.to_datetime(df["time"], format = '%Y-%m')
df["cell_value"] = [float(str(i).replace(",","")) for i in df["cell_value"]]
df["cell_value"] = df["cell_value"].map(lambda x: float(x))
df["month"] = df["time"].map(lambda x: x.strftime("%B"))

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

durable_goods_orders = durable_goods_orders.sort_values(by = "time", ascending=False)
durable_goods_orders = durable_goods_orders.reset_index()
durable_goods_orders = durable_goods_orders.drop(columns= "index")

headline = durable_goods_orders[durable_goods_orders["Report"] == "Headline durable goods orders"]
headline = headline.reset_index().drop(columns = "index")
headline["m/m"] = headline["cell_value"].diff(periods = -1)

ex_transport = durable_goods_orders[durable_goods_orders["Report"] == "Durable Goods (ex. transportation"]
ex_transport = headline.reset_index().drop(columns = "index")
ex_transport["m/m"] = ex_transport["cell_value"].diff(periods = -1)

core = durable_goods_orders[durable_goods_orders["Report"] == "Core durable goods orders (ex. defense and aircraft)"]
core = headline.reset_index().drop(columns = "index")
core["m/m"] = core["cell_value"].diff(periods = -1)

core_ship = durable_goods_orders[durable_goods_orders["Report"] == "Core capital goods shipments (which feeds into GDP"]
core_ship = headline.reset_index().drop(columns = "index")
core_ship["m/m"] = core_ship["cell_value"].diff(periods = -1)

# TK - run tables and text outputs below through loop
t = ["headline","ex_transport","core","core_ship"]
t = list(zip(t, rpt_list))

"""# Tables"""

def print_statements():
  if headline["m/m"][0] > 0:
    print("{} {} rose {}pp m/m to {}%.".format(headline["month"][0], headline["Report"][0], headline["cell_value"][0]))
  elif headline["m/m"][0] < 0:
    print("{} {} fell {}pp m/m to {}%.".format(headline["month"][0], headline["Report"][0], headline["cell_value"][0]))
  elif headline['m/m'][0] == 0:
    print("{} {} was unchangedm/m at {}%.".format(headline["month"][0], headline["Report"][0], headline["cell_value"][0]))

headline_vs_est = ()
if headline["m/m"][0] > headline_est:
  headline_vs_est = "beating"
elif headline["m/m"][0] < headline_est:
  headline_vs_est = "missing"
elif headline["m/m"][0] == headline_est:
  headline_vs_est = "in line with estimates"

vs_prior = ()
if headline["cell_value"][0] > headline["cell_value"][1]:
  vs_prior = "up from"
if headline["cell_value"][0] > headline["cell_value"][1]:
  vs_prior = "down from"
if headline["cell_value"][0] == headline["cell_value"][1]:
  vs_prior = "unchanged from"

rose_fell = ()
if headline["m/m"][0] > 0:
  rose_fell = "rose"
elif headline["m/m"][0] < 0:
  rose_fell = "fell"
elif headline["m/m"][0] == 0:
  rose_fell = "was unchanged m/m at"

if headline["m/m"][0] == 0:
  print("{} {} {} {}%, {} estimates for {}% and {} {} {}% print.".format(headline["month"][0], headline["Report"][0], rose_fell, headline["m/m"][0], headline["cell_value"][0], headline_vs_est, headline_est, vs_prior, headline["month"][1], headline["cell_value"][1]))
else:
  print("{} {} {} {}pp m/m to {}%, {} estimates for {}% and {} {} {}% print.".format(headline["month"][0], headline["Report"][0], rose_fell, headline["m/m"][0], headline["cell_value"][0], headline_vs_est, headline_est, vs_prior, headline["month"][1], headline["cell_value"][1]))

ex_transport

core

core_ship