import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
import os


#Load data set, set 'usecols' to columns for PCA use
data = pd.read_csv('filename.csv', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])

#convert it to numpy arrays
X=data.values

#Scaling the values
X = scale(X)

pca = PCA(n_components=20)

pca.fit(X)

#The amount of variance that each PC explains
var= pca.explained_variance_ratio_

#Cumulative Variance explains
var1=np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)

print ("The amount of variance that each PC explains:", var)
print ("Cumulative Variance explains:", var1)
#print ("mean:", pca.mean_)

plt.plot(var1)


#Looking at above plot I'm taking 10 variables
pca = PCA(n_components=10)
pca.fit(X)

print("components:" , pca.components_)
X1=pca.fit_transform(X)

print (X1)

subplots_adjust(hspace=0.2, top=2, bottom=0)
number_of_subplots= len(pca.components_)

for i,v in enumerate(xrange(number_of_subplots)):
    v = v+1
    plt.subplot(number_of_subplots,1,v)
    x = range(1, len(X[0])+1)
    y = pca.components_[i]
    plt.bar(x, y, color='r')

plt.show()

#create "outfile.txt" file

np.savetxt('sh1.csv',(var,), delimiter = ",", fmt = "%5.2f")

#set d to number of PCs taken: 10
d = [1,2,3,4,5,6,7,8,9,10, 'breach']
np.savetxt('sh2.csv',(d,), delimiter = ",", fmt = "%s")

#enter in breach column, set 'usecols' to breach column
breachValues = pd.read_csv('filename.csv', usecols = [10])
X1_breachValues = np.concatenate((X1, breachValues.values), axis = 1)
np.savetxt('sh3.csv', X1_breachValues, delimiter = ",", fmt = "%5.2f")

fout=open("outfile.txt","a")    
for num in range(1,4):
    f = open("sh"+str(num)+".csv")
    #f.next() # skip the header
    for line in f:
         fout.write(line)
    f.close()
    os.remove("sh"+str(num)+".csv")
fout.close()
