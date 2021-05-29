import requests
import pandas as pd
import numpy as np
import datetime
import dateutil

# Add prior month's unrevised data and estimates:

month = "2021-04-01"
rpt_list = ["Headline durable goods orders", "Durable Goods (ex. transportation)", "Core durable goods orders (ex. defense and aircraft)", "Core capital goods shipments (which feeds into GDP"]
prior_unrevised = [1.0, 2.3, 0.5, 1.5]
estimate = [0.8, 0.7, np.nan, np.nan]

time = pd.to_datetime(month, format ='%Y-%m')
m = [month, month, month, month]
df2 = pd.DataFrame(zip(m, rpt_list, prior_unrevised, estimate), columns=["time", "report", "prior_unrevised", "estimate"])

df2

"""# Code - to pull key Durable Goods Orders indicators"""

base_url = "https://api.census.gov/data/timeseries/eits/advm3?get=data_type_code,time_slot_id,seasonally_adj,category_code,cell_value,error_data&for=us:*&time=from+{}".format("2020-03")
response = requests.get(base_url)
data = response.json()
df = pd.DataFrame(data[1:], columns = data[0])

df["time"] = pd.to_datetime(df["time"], format = '%Y-%m')
df["cell_value"] = [float(str(i).replace(",","")) for i in df["cell_value"]]
df["cell_value"] = df["cell_value"].map(lambda x: float(x))
df["month"] = df["time"].map(lambda x: x.strftime("%B"))

rpt_list = ["Headline durable goods orders", "Durable Goods (ex. transportation)", "Core durable goods orders (ex. defense and aircraft)", "Core capital goods shipments (which feeds into GDP"]
data_type_code = ["MPCNO", "MPCNO", "MPCNO", "MPCVS"]
category_code = ["MDM", "DXT", "DXD", "NXA"]
cols = ["report", "data_type_code","category_code"]
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

headline = durable_goods_orders[durable_goods_orders["report"] == "Headline durable goods orders"]
headline = headline.reset_index().drop(columns = "index")
headline["m/m"] = headline["cell_value"].diff(periods = -1)
headline["rose/fell"] = np.where(headline["cell_value"] == 0, " was unchanged", np.where(headline["cell_value"] > 0, "rose", "fell"))
headline["vs_prior"] = np.where(headline["m/m"] > 0, "up from", np.where(headline["m/m"] == 0, "unchanged from", "down from"))

ex_transport = durable_goods_orders[durable_goods_orders["report"] == "Durable Goods (ex. transportation)"]
ex_transport = ex_transport.reset_index().drop(columns = "index")
ex_transport["m/m"] = ex_transport["cell_value"].diff(periods = -1)
ex_transport["rose/fell"] = np.where(ex_transport["cell_value"] == 0, "was unchanged", np.where(ex_transport["cell_value"] > 0, "rose", "fell"))
ex_transport["vs_prior"] = np.where(ex_transport["m/m"] > 0, "up from", np.where(ex_transport["m/m"] == 0, "unchanged from", "down from"))

core = durable_goods_orders[durable_goods_orders["report"] == "Core durable goods orders (ex. defense and aircraft)"]
core = core.reset_index().drop(columns = "index")
core["m/m"] = core["cell_value"].diff(periods = -1)
core["rose/fell"] = np.where(core["cell_value"] == 0, "was unchanged", np.where(core["cell_value"] > 0, "rose", "fell"))
core["vs_prior"] = np.where(core["m/m"] > 0, "up from", np.where(core["m/m"] == 0, "unchanged from", "down from"))

core_ship = durable_goods_orders[durable_goods_orders["report"] == "Core capital goods shipments (which feeds into GDP"]
core_ship = core_ship.reset_index().drop(columns = "index")
core_ship["m/m"] = core_ship["cell_value"].diff(periods = -1)
core_ship["rose/fell"] = np.where(core_ship["cell_value"] == 0, "was unchanged", np.where(core_ship["cell_value"] > 0, "rose", "fell"))
core_ship["vs_prior"] = np.where(core_ship["m/m"] > 0, "up from", np.where(core_ship["m/m"] == 0, "unchanged from", "down from"))

currentmonth = pd.merge((durable_goods_orders[durable_goods_orders["time"] == time]), df2, how = "left", left_on= "report", right_on = "report")
currentmonth["vs_est"] = np.where(currentmonth["cell_value"] == currentmonth["estimate"], "in line with",
                                  np.where(currentmonth["cell_value"] > currentmonth["estimate"], "beating", "missing"))
# Add blank if cell equals NaN
currentmonth

# Print statements

print("{} {} {} {}%, {} estimates for {}%, {} revised {} {}% (was {}%).".format(headline["month"][0],
                            headline["report"][0],
                            headline["rose/fell"][0],
                            headline["cell_value"][0],
                            currentmonth.set_index("report").loc["Headline durable goods orders"]["vs_est"],
                            currentmonth.set_index("report").loc["Headline durable goods orders"]["estimate"],
                            headline["vs_prior"][0],
                            headline["month"][1],
                            headline["cell_value"][1],
                            currentmonth.set_index("report").loc["Headline durable goods orders"]["prior_unrevised"]))

currentmonth.set_index("report").loc["Headline durable goods orders"]["vs_est"]

# Tables

headline

ex_transport

core

core_ship
