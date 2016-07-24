import csv
import numpy as np
from itertools import islice

class Bin:
	def __init__(self, left_boundary, right_boundary):
		self.left_boundary = float(left_boundary)
		self.right_boundary = float(right_boundary)
		self.count = 0
		self.center = (self.left_boundary + self.right_boundary) / 2


	def random_sample(self):
		return np.random.normal(loc=self.center, scale=abs(self.center - self.left_boundary))

def bin_establish(input_csv_name):
	with open(input_csv_name, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)
		iter = (islice(csv_reader, 0, None))	
		eig_values = next(iter)
		list_min_max = []
		for i in range(len(eig_values)):
			list_min_max.append({'min' : 0, 'max': 0})
		first_row = next(iter)
		for index in range(0, len(first_row)):
			list_min_max[index]['min'] = float(first_row[index])
			list_min_max[index]['max'] = float(first_row[index])
		for row in iter:
			for index in range(0, len(row)):
				if float(row[index]) < float(list_min_max[index]['min']):
					list_min_max[index]['min'] = float(row[index])
				elif float(row[index]) > float(list_min_max[index]['max']):
					list_min_max[index]['max'] = float(row[index])
	list_min_max

