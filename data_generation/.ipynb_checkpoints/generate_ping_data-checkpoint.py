import numpy as np
import pandas as pd
import random

rng = np.random.default_rng(42)

records = 10

lat_min,lat_max = 17.20,17.80
log_min,log_max = 78.35,78.95

datetime1 = pd.Timestamp('2026-11-01 06:00:00')
datetime2 = pd.Timestamp('2026-11-02 00:00:00')

ping = 10

data = []
ping_id = 1
for i in range(records):
  dev_id = f"dev_{i+1:02d}"
   # Reserve time for all pings
  latest_start = datetime2 - pd.Timedelta(minutes=10 * ping)

  times = random.uniform(
        datetime1.timestamp(),
        latest_start.timestamp()
    )

  timestamp = datetime1 + pd.Timedelta(
        seconds=times - datetime1.timestamp()
    )
  lat = rng.uniform(lat_min,lat_max)
  log = rng.uniform(log_min,log_max)

  for z in range(ping):
      movement = rng.choice(['stationary', 'walking', 'cycling', 'driving'],
                               p=[0.20,0.30,0.20,0.30])
      if movement == 'stationary':
        speed = 0
      elif movement == 'walking':
        speed = rng.uniform(2,5)
      elif movement == 'cycling':
        speed = rng.uniform(8,20)
      elif movement == 'driving':
        speed = rng.uniform(30,50)

      interval = int(rng.integers(1,11))
      angel = rng.uniform(0,2*np.pi)
      distance = speed *interval/60

      delta_lat = (distance/111.32)*np.cos(angel)
      delta_log = (
            distance / (111.32 * np.cos(np.radians(lat)))
        ) * np.sin(angel)

      #Keep coordinates within simulation bounds
      lat = np.clip(lat + delta_lat, lat_min, lat_max)
      log = np.clip(log + delta_log, log_min, log_max)
      timestamp += pd.Timedelta(minutes=interval)

      data.append([
            ping_id,
            dev_id,
            round(lat, 5),
            round(log, 5),
            timestamp,
            round(speed, 2),
            movement,
            "Hyderabad"
        ])

      ping_id += 1


df = pd.DataFrame(data, columns=('ping_id', 'device_id','latitude', 'longtitude','timestamp', 'speed', 'movement', 'city'))

df.to_csv("sample_data.csv", index= False)