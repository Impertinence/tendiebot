import coinbasepro as cbp

import matplotlib.pyplot as plt
import numpy as np

import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
intervals = datetime.timedelta(minutes=300)
previous = datetime.datetime.strptime(now, "%Y-%m-%d %H:%M") - intervals

public_client = cbp.PublicClient()

last_5_hrs = public_client.get_product_historic_rates("BTC-USD", previous, now, 60)

fig, axes = plt.subplots()

time = [entry['time'].strftime("%Y-%m-%d %H:%M") for entry in last_5_hrs]
high_price = [str(entry['high']) for entry in last_5_hrs]

axes.plot(time, high_price)
plt.show()