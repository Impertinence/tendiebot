from finance import data_generation

generate_data = data_generation.GenerateData()

#Populate relevant collections with data
generate_data.PopulateCollections("stock", [
    ["tsla", "amd", "pltr"],
    "hour",
    "month",
    "regular"
])