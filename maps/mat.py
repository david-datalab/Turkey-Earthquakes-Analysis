
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns 


terror_data = pd.read_csv('./eq1/data/records.csv', encoding='ISO-8859-1',
                          usecols=[0, 1, 2, 3,])

terror_sl = terror_data[(terror_data.country_txt == 'Sri Lanka')]
lon_min, lon_max = 79, 82
lat_min, lat_max = 5, 10

idx_sl = (terror_sl["longitude"]>lon_min) &\
            (terror_sl["longitude"]<lon_max) &\
            (terror_sl["latitude"]>lat_min) &\
            (terror_sl["latitude"]<lat_max)
            
terror_attacks_lk = terror_sl[idx_sl].sample(n=1000)
            
# Mercator of China
plt.figure(2, figsize=(20,10))

m2 = Basemap(projection='merc',
             llcrnrlat=lat_min,
             urcrnrlat=lat_max,
             llcrnrlon=lon_min,
             urcrnrlon=lon_max,
             lat_ts=35,
             resolution='i')

m2.fillcontinents(color='yellow',lake_color='#000000') # yellow land, black lakes
m2.drawmapboundary(fill_color='#68d4f2')                # light blue
m2.drawcountries(linewidth=0.3, color="w")              # thin white line for country borders

# Plot the data
mxy = m2(terror_attacks_lk["longitude"].tolist(), terror_attacks_lk["latitude"].tolist())
m2.scatter(mxy[0], mxy[1], s=5, c="#ff0019", lw=0, alpha=0.5, zorder=5)

plt.title("Sri Lanka view of events")
plt.show()                          