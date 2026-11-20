import pandas as pd
import random

random.seed(42)

records=5000

lat_min,lat_max = 17.20,17.80
log_min,log_max = 78.35,78.95


store =[]

for i in range(records):
    store_id = f"store_{i+1:04d}"
    lat = round(random.uniform(lat_min,lat_max),5)
    log = round(random.uniform(log_min,log_max),6)
    city = 'hyderabad'

    store.append([store_id,lat,log,city])

df = pd.DataFrame(store, columns = ['store_id','latitude','longtitude','city'])

df.to_csv("store_data.csv", index = False)