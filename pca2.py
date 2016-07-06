import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale



#Load data set
data = pd.read_csv('placesrated2.csv')

#convert it to numpy arrays
X=data.values

#Scaling the values
X = scale(X)

pca = PCA(n_components=9)

pca.fit(X)

#The amount of variance that each PC explains
var= pca.explained_variance_ratio_

#Cumulative Variance explains
var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)

print ("The amount of variance that each PC explains:", var)
print ("Cumulative Variance explains:", var1)
#print ("mean:", pca.mean_)

plt.plot(var1)

9

#Looking at above plot I'm taking 30 variables
pca = PCA(n_components=7)
pca.fit(X)

print("components:" , pca.components_)
X1=pca.fit_transform(X)

#print (X1)

subplots_adjust(hspace=0.2, top=2, bottom=0)
number_of_subplots= len(pca.components_)

for i,v in enumerate(xrange(number_of_subplots)):
    v = v+1
    plt.subplot(number_of_subplots,1,v)
    x = range(1, len(X[0])+1)
    y = pca.components_[i]
    plt.bar(x, y, color='r')

plt.show()