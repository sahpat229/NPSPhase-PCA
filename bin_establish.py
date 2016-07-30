import csv
import numpy as np
from itertools import islice

'''
Bin class, each bin instance has a left boundary, a right boundary, a counter, a center,
and a function called random_sample.
'''


class Bin:
	def __init__(self, left_boundary, right_boundary):
		self.left_boundary = float(left_boundary)
		self.right_boundary = float(right_boundary)
		self.count = 0
		self.center = (self.left_boundary + self.right_boundary) / 2


	def random_sample(self):
		return np.random.normal(loc=self.center, scale=abs(self.center - self.left_boundary))



def bin_establish(input_csv_name, number_of_bins):
	with open(input_csv_name, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)
		iter = islice(csv_reader, 0, None)	
		eig_values = next(iter)
		#print "LENGTH: ", len(eig_values)
		del eig_values[-1]
		list_min_max = []

		for i in range(len(eig_values)):
			list_min_max.append({'min' : 0, 'max': 0})

		#put whether next(next(iter)) below if headers will be used
		next(iter)
		first_row = next(iter)
		del first_row[-1]
		#print "FIRST ROW: ", first_row
		for index in range(0, len(first_row)):
			list_min_max[index]['min'] = float(first_row[index])
			list_min_max[index]['max'] = float(first_row[index])

		for row in iter:
			del row[-1]
			#print "ROW: ", row
			for index in range(0, len(row)):
				if float(row[index]) < float(list_min_max[index]['min']):
					list_min_max[index]['min'] = float(row[index])
				elif float(row[index]) > float(list_min_max[index]['max']):
					list_min_max[index]['max'] = float(row[index])

		#print "LIST MINMAX: ", list_min_max
	list_of_list_of_bins = []

	for min_max in list_min_max:
		list_of_bins = []
		total_length = min_max['max'] - min_max['min']
		bin_length = total_length / number_of_bins
		current_length = min_max['min']

		for i in range(number_of_bins):
			list_of_bins.append(Bin(current_length, current_length+bin_length))
			current_length += bin_length

		list_of_list_of_bins.append(list_of_bins)

	with open(input_csv_name, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)
		iter = islice(csv_reader, 0, None)
		next(iter)
		next(iter)
		next(iter)
		for row in iter:
			del row[-1]
			for index in range(0, len(row)):
				current_item = row[index]
				for bin in list_of_list_of_bins[index]:
					if (current_item >= bin.left_boundary) and (current_item =< bin.right_boundary):
						bin.count += 1
						break

	
	total_counts = []
	for list_of_bins in list_of_list_of_bins:
		total_count = 0
		for bin in list_of_bins:
			total_count += bin.count
		total_counts.append(total_count)


	return (list_of_list_of_bins, total_counts)

def test_bin_establish(input_csv_name, number_of_bins):
	(list_of_list_of_bins, total_counts) = bin_establish(input_csv_name, number_of_bins)
	for list_of_bins in list_of_list_of_bins:
		for bin in list_of_bins:
			print bin.left_boundary, bin.right_boundary
		print "---------------------------------------------------------------"
