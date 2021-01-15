from finance import data_generation

generate_data = data_generation.GenerateData()

#Populate relevant collections with data
# generate_data.PopulateHistoricalCollections("stock", [
#     ["tsla", "amd", "pltr"],
#     "hour",
#     "month",
#     "regular"
# ])

#Populate Analyses Table

eth_daily_data = generate_data.PopulateCryptoHistorical([
    "eth",
    "5minute",
    "day",
    "24_7"
])

hourly_data = generate_data.PopulateCryptoHistorical([
    "eth",
    "15second",
    "hour",
    "24_7"
])

print(hourly_data)