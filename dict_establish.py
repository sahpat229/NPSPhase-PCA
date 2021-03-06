import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import csv
import math
from itertools import islice

'''
Wariness dictates the starting probability of the core and the geometric scaling
of the core
'''

def wariness_to_core_probability_and_scaling(wariness):
	core_probability = 0.25
	# core_probability = func(wariness)
	scaling = 1.0 - core_probability
	return (core_probability, scaling)

'''
Function defining Gaussian-like probability dist, left or right demarcates
which tail it is, either the left tail for the core region or the right tail

Evaluates the probability of x for the Gaussian-like probability distribution
'''

def probability_dist(mu_value, mu, sigma_squared, x):
	exponent = -1.0 * ((x - mu)**2) / (2.0*sigma_squared)
	return mu_value * math.exp(exponent)


class Point:

	'''
	A point is initialized with a wariness level, and influence region level, and a zipped
	fields array along with their respective eigenvalue fractions
	'''

	def __init__(self, wariness, influence_region, fields_array_with_eig_fractions, core_radius, breach_value):
		(self.core_probability_static, self.core_scaling) = wariness_to_core_probability_and_scaling(wariness)
		self.core_probability = self.core_probability_static * (breach_value / 2.0)
		self.fields_and_eigs = fields_array_with_eig_fractions
		self.core_radius = core_radius
		self.core_fields_radii = []
		self.center = []
		self.influence_region = influence_region
		self.influence_region_radii = []
		self.breach_value = breach_value

		#print "self.fields_and_eigs: ", self.fields_and_eigs
		for tuple in self.fields_and_eigs:
			self.core_fields_radii.append(tuple[1] *  self.core_radius)
			self.center.append(tuple[0])
			self.influence_region_radii.append(tuple[1] * self.influence_region)

	'''
	checks if argument fields_iter falls within this instance's influence region
	will be used like:
	for point in Points:
		if point.influence_check(current_fields_arr_iter) == 'True':
			point.prob_increase()
			break
		else
			//Initialize a new Point at this point demarcated by fields_arr
	'''

	def influence_check(self, other_fields_arr):
		for (this_inf_radii, this_center, other_fields) in zip(self.influence_region_radii, self.center, other_fields_arr):
			#print this_inf_radii, this_center, other_fields
			if (other_fields > (this_center + this_inf_radii)) or (other_fields < (this_center - this_inf_radii)):
				return False
		return True

	'''
	Generator that will increase the core_probability
	Should be called when a new point falls in a previous point's influence region
	'''
	def increase_core_probability(self, breach_value):
		#print "INCREASED", "BREACH VALUE: ", breach_value
		self.core_probability += (self.core_probability_static * (breach_value / 2.0) * self.core_scaling)
		#print "NEW PROB: ", self.core_probability

	'''
	Function for plotter
	Returns the probability of "X" against this point given a component number
	'''
	def probability_component(self, component_number, x):
		left_core_side = self.center[component_number] - self.core_fields_radii[component_number]
		right_core_side = self.center[component_number] + self.core_fields_radii[component_number]
		left_influence_side = self.center[component_number] - self.influence_region_radii[component_number]
		right_influence_side = self.center[component_number] + self.influence_region_radii[component_number]
		left_sigma = abs(left_core_side - left_influence_side)
		right_sigma = abs(right_influence_side - right_core_side)

		if left_core_side <= x <= right_core_side:
			return self.core_probability

		elif x < left_core_side:
			return probability_dist(self.core_probability, left_core_side, left_sigma**2, x)

		elif x > right_core_side:
			return probability_dist(self.core_probability, right_core_side, right_sigma**2, x)


	'''
	returns the probability of breach at a certain point demarcated by
	component_value on the axis demarcated by component_number

	This probability is dictated by a uniform distribution in the core
	with Gaussian-like tails, Each tail has a mu = core_boundary, and 
	sigma_squared = influence_region_bndry
	'''


	def probability(self, other_fields_arr):

		total_prob = 0

		for (component_number, component_value) in zip(range(len(other_fields_arr)), other_fields_arr):
			#print "NO: ", component_number, "VAL: ", component_value
			left_core_side = self.center[component_number] - self.core_fields_radii[component_number]
			right_core_side = self.center[component_number] + self.core_fields_radii[component_number]
			left_influence_side = self.center[component_number] - self.influence_region_radii[component_number]
			right_influence_side = self.center[component_number] + self.influence_region_radii[component_number]
			left_sigma = abs(left_core_side - left_influence_side)
			right_sigma = abs(right_influence_side - right_core_side)

			if left_core_side <= component_value <= right_core_side:
				total_prob += self.core_probability

			elif component_value < left_core_side:
				total_prob += probability_dist(self.core_probability ,left_core_side, left_sigma**2, component_value)

			elif component_value > right_core_side:
				total_prob += probability_dist(self.core_probability, right_core_side, right_sigma**2, component_value)

		return total_prob / len(other_fields_arr)

'''
Establishes a distribution space for the CSV file demarcated by input_csv_name
input_csv_name should be a csv file that was generated through PCA, as each components
eigenvalues will be used with it

Returns both list_of_points and eigenvalue_fractions so that mcsim.py can use eigenvalue_fractions
when doing a weighted distance calculation

'''

def dist_establish(input_csv_name, wariness, influence_region, core_radius):
	with open(input_csv_name, 'r') as csv_file:		
		csv_reader = csv.reader(csv_file)
		list_of_points = []
		iter = islice(csv_reader, 0, None)
		eigenvalue_fractions = next(iter)
		del eigenvalue_fractions[-1]
		eigenvalue_fractions = map(float, eigenvalue_fractions)
		next(iter)
		initial_row = map(float, (next(iter)))
		breach_value = initial_row[len(initial_row) - 1]
		del initial_row[-1]
		initial_fields_array_with_eig_fractions = zip(initial_row, eigenvalue_fractions)
		point = Point(wariness, influence_region, initial_fields_array_with_eig_fractions, core_radius, breach_value)
		list_of_points.append(point)
		for row in iter:

			row = map(float, row)
			breach_value = row[len(row) - 1]
			del row[-1]
			#print "ROW: ", row
			for point in list_of_points:
				if point.influence_check(row):
					point.increase_core_probability(breach_value)
					break
			else:
				fields_array_with_eig_fractions = zip(row, eigenvalue_fractions)
				point = Point(wariness, influence_region, fields_array_with_eig_fractions, core_radius, breach_value)
				list_of_points.append(point)

		return (list_of_points, eigenvalue_fractions)