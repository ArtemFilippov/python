import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

data = pd.read_csv("https://video.ittensive.com/python-advanced/data-9753-2019-07-25.utf.csv", sep=";", na_values="NA", decimal=",")
data = pd.DataFrame({"UnemployedDisabled": data["UnemployedDisabled"], "UnemployedTotal" :data["UnemployedTotal"], "Year" : data['Year'], "Month" : data['Period']})
data = data.groupby("Year").filter(lambda x: x["Year"].count() >= 6)
data_group = data.groupby("Year").mean()

data_group["Rel"] = data_group["UnemployedDisabled"] / data_group["UnemployedTotal"];

x = np.array(data_group.index).reshape(len(data_group.index), 1)
y = np.array(data_group["Rel"]).reshape(len(data_group["Rel"]), 1)

model = LinearRegression()
model.fit(x, y)

#plt.scatter(x, y,  color='orange')
#x = np.append(x, [2020]).reshape(len(data_group.index)+1, 1)
#plt.plot(x, model.predict(x), color='blue', linewidth=3)
#plt.show()

predict = model.predict(np.array(2020).reshape(1, 1))[0][0]
print (round(predict*100,2))

print(model.coef_, model.intercept_)
input()
