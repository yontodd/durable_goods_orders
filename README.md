# durable_goods_orders

Latest update - May 29, 2021
* Enter consensus estimates and previous (unrevised) report data into a table
* Statement now compares headline print to both estimates and prior month, and now compares prior month to revisions

Key US economic datapoints from Census Bureau's monthly Advance Report on Durable Goods Manufacturers' Shipments, Inventories, and Orders

Pulls key data points from monthly Advance Durable Goods report from the US Census Bureau's API (https://www.census.gov/developers/).

Pulls the two most recent monthly datapoints for:
* Headline durable goods orders
* Durable goods orders (ex. Transporation)
* Core durable goods order (ex. defense and aircraft)
* Core capital goods shipments

Other available Census Bureau timeseries (https://api.census.gov/data/timeseries.html)

To-dos:
* Print statement for Orders ex-transports
* Add revisions to prior month's data
