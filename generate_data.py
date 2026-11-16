import numpy as np
import pandas as pd
import random

records = 10

lat_min,lat_max = 17.20,17.80
log_min,log_max = 78.35,78.95

datetime1 = pd.Timestamp('2026-11-01 06:00:00')
datetime2 = pd.Timestamp('2026-11-02 00:00:00')

data = []
for i in range(records):
  dev_id = f"dev_{i+1:02d}"
  for j in range(records):
    lat= round(random.uniform(lat_min,lat_max),5)
    log = round(random.uniform(log_min,log_max),5)
    times =random.uniform(datetime1,datetime2)
    timestamp = pd.Timestamp(times)
    data.append([dev_id,lat,log,timestamp])

df = pd.DataFrame(data, columns=('device_id','longitude', 'longtitude','timestamp'))

df.to_csv("sample_data.csv", index= False)