import numpy as np
import matplotlib.pyplot as plt
from pylab import *

np.set_printoptions(precision = 5)

x = np.array([[4.0, 4.2, 3.9, 4.3, 4.1], [2.0, 2.1, 2.0, 2.1, 2.2], [0.60,
	0.59, 0.58, 0.62, 0.63]])

def mean_vector(matrix):
	return np.mean(matrix, axis=1)

def column_multiply(col):  #multiply column by transpose of column
	matr = np.zeros((col.shape[0], col.shape[0]))
	for i in range(col.shape[0]):
		for j in range(len(col)):
			matr[i, j] = col[i]*col[j]
	#print "Matr", matr
	return matr


def scatter_matr(matrix):
	scatter_matr = np.zeros((matrix.shape[0], matrix.shape[0]))
	#print mean_vector(matrix)
	for i in range(matrix.shape[1]):
		scatter_matr += column_multiply(matrix[:, i] - mean_vector(matrix))
		#print "Scatter_matr", scatter_matr
	scatter_matr = (1.0/(matrix.shape[1] -1 ))*scatter_matr
	return scatter_matr

class Tupled_Eigvals:
	def __init__(self, w):
		#eigs = np.ndarray(shape=w.shape, dtype=object)
		self.eigtuples = []
		self.total = 0
		for i in range(len(w)):
			self.eigtuples.append((w[i], i))
			self.total += w[i]
		self.eigtuples = sorted(self.eigtuples, key=lambda x: x[0], reverse = True)
		self.eigtuples = np.array(self.eigtuples)

	def determine_components(self, threshhold):
		if threshhold > 1:
			raise EnvironmentError
		summation = 0
		for i in range(len(self.eigtuples)):
			summation += self.eigtuples[i][0]
			if (summation / self.total) >= threshhold :
				#print "num comopnents: ", i
				return i
			else:
				continue

	def sort_eigenvectors(self, eigenvector_matrix):
		self.eigenvectors = np.zeros(shape=eigenvector_matrix.shape)
		i = 0
		for eigentuple in self.eigtuples:
			self.eigenvectors[i] = eigenvector_matrix[:, eigentuple[1]]
			i = i + 1

def obtain_eigenvalues(matrix):
	w, v = np.linalg.eig(matrix)
	return (w,v)




scatter_matrix = scatter_matr(x)
eigs = obtain_eigenvalues(scatter_matrix)
print "eigenvalues: ", eigs[0]
print "Before eigenvectors: ", eigs[1]
tups = Tupled_Eigvals(eigs[0]) 	
tups.sort_eigenvectors(eigs[1])
print "After eigenvectors: ", tups.eigenvectors
print "Self.eigtuples: ", tups.eigtuples, "len of eigtuples: ", len(tups.eigtuples)
print "total: ", tups.total
component_limit = tups.determine_components(0.95)

# x = np.linspace(0, 2*np.pi, 400)
# y = np.sin(x**2)

subplots_adjust(hspace=0.000)
number_of_subplots= component_limit + 1

for i,v in enumerate(xrange(number_of_subplots)):
    v = v+1
    plt.subplot(number_of_subplots,1,v)
    x = range(1, len(eigs[0]) + 1)
    y = tups.eigenvectors[i]
    plt.bar(x, y, color='r')

plt.show()
