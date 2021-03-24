import datetime

now = ((datetime.datetime.now() + datetime.timedelta(hours=4)) - datetime.datetime(1970, 1, 1)).total_seconds()
interval = (datetime.timedelta(minutes=300)).total_seconds()

test = (datetime.datetime(2021, 3, 15, 5, 3) - datetime.datetime(1970, 1, 1)).total_seconds()

print(int((now - test) / interval))