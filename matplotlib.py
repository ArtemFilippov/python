import geopandas as gpd
import pandas as pd
import descartes
import gzip
import json
import requests
import io
import matplotlib.pyplot as plt
import pylab as plot
import numpy as np
from matplotlib.font_manager import FontProperties

import matplotlib.ticker as ticker

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
plt.rcParams['axes.formatter.useoffset'] = False

data_obj = pd.read_csv("C:/Users/1/Desktop/dz/data-44-structure-4.csv.gz",compression='gzip', na_values=['NA'],sep=',',low_memory=False)
data_res = pd.DataFrame({"DISTRICT" : data_obj['Регион']})

data_res["cnt"] = 1


data_group = data_res.groupby(["DISTRICT"]).agg("count")
data_group = data_group.reset_index()

t =  data_group["DISTRICT"].values
y = []

for el in t:
	if(el == "Республика Адыгея (Адыгея)"):
		y.append("РЕСПУБЛИКА АДЫГЕЯ")
	elif(el == "Республика Марий Эл"):
		y.append("РЕСПУБЛИКА МАРИЙ-ЭЛ")
	elif(el == "Республика Северная Осетия - Алания"):
		y.append("РЕСПУБЛИКА СЕВЕРНАЯ ОСЕТИЯ")
	elif(el == "Республика Татарстан (Татарстан)"):
		y.append("РЕСПУБЛИКА ТАТАРСТАН")
	elif(el == "Ханты-Мансийский автономный округ - Югра"):
		y.append("ХАНТЫ-МАНСИЙСКИЙ АВТОНОМНЫЙ ОКРУГ")
	elif(el == "Чувашская Республика - Чувашия"):
		y.append("ЧУВАШСКАЯ РЕСПУБЛИКА")
	else:
		y.append(el)
		
data_group["DISTRICT"] = y


data_group["DISTRICT"] = data_group["DISTRICT"].str.upper()

link = 'https://video.ittensive.com/python-advanced/russia.json'
data = gpd.read_file(link)
data = data.to_crs({'init':'epsg:3857'})


data = pd.merge(left=data, right=data_group, left_on="NL_NAME_1", right_on="DISTRICT", how="left")
data["TITLE"] = data_group["DISTRICT"].astype(str) + ": " + round(data_group["cnt"],1).astype(str)

fig = plt.figure(figsize=(16,16))
(area1, area2, area3) = fig.subplots(3, 1, gridspec_kw={'height_ratios': [2, 0.5, 2]})


area1.set_xlim(0, 2e7)
data.plot(ax=area1, legend=True, column="cnt", cmap='tab20')

area2.set(xticks=[], yticks=[])
area3.set(xticks=[], yticks=[])
area2.tick_params(color='green', labelcolor='green')
area3.tick_params(color='green', labelcolor='green')


i = 0
l = len(data["TITLE"])
t1=""
t2=""
t3=""
t4=""
for el in data["TITLE"]:
	if i < l/4:
		t1 = t1 + el + "\n"
	elif i >= l/4 and i < l/2 :
		t2 = t2 + el + "\n"
	elif i >= l/2 and i < (3*l)/4 :
		t3 = t3 + el + "\n"
	else:
		t4 = t4 + el + "\n"
	i = i+1

area3.text(0.1, 0.1, t1, horizontalalignment = 'left',color = 'black', fontsize = 6)
area3.text(0.3, 0.1, t2, horizontalalignment = 'left',color = 'black', fontsize = 6)
area3.text(0.5, 0.1, t3, horizontalalignment = 'left',color = 'black', fontsize = 6)
area3.text(0.7, 0.1, t4, horizontalalignment = 'left',color = 'black', fontsize = 6)

area2.set_axis_off()
area1.set_axis_off()
area3.set_axis_off()
fig.tight_layout(pad=3, w_pad=3, h_pad=3)

plt.show()

input()
