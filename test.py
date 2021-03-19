import coinbasepro as cbp
import datetime

now = datetime.datetime.now()

public_client = cbp.PublicClient()

print(len(public_client.get_product_historic_rates("BTC-USD", )))