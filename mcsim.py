from dict_establish import Point
from bin_establish import Bin
import random
import math

'''
Takes a list_of_list_of_bins generated by bin_establish and a total_counts list generated by
bin_establish, and generates the probability for picking a bin, (i.e., the first "roll") for each
field
'''


def sampling_for_which_bin(list_of_list_of_bins, total_counts):
	probs_of_bins_for_each_field = []
	for index in range(len(list_of_list_of_bins)):
		list_of_bins = list_of_list_of_bins[index]
		total_count = total_counts[index]
		probs_for_this_field = []
		for bin in list_of_bins:
			probs_for_this_field.append(float(bin.count) / float(total_count))
		probs_of_bins_for_each_field.append(probs_for_this_field)

	return probs_of_bins_for_each_field


'''
Takes a list_of_list_of_bins and a probs_of_bins_for_each_field and generates a sample,
which is basically an array of components, to be used 
'''

def generate_a_sample(list_of_list_of_bins, probs_of_bins_for_each_field):
	random.seed()

	fields_arr = []

	for index in range(len(list_of_list_of_bins)):
		list_of_bins = list_of_list_of_bins[index]
		probs_for_this_field = probs_of_bins_for_each_field[index]
		random_numb = random.randrange(0, 100)
		random_numb /= 100
		for index in range(0, len(probs_for_this_field)):
			random_numb -= probs_for_this_field[index]
			if random_numb <= 0:
				selected_bin = list_of_bins[index]
				fields_arr.append(selected_bin.random_sample())
				break

	return fields_arr

'''
takes a single eig_fraction and inverts it, to be used with map to invert the eig_fractions
array when doing a weighted analysis of the distances
'''

def invert(eig_fraction):
	return 1.0 / eig_fraction

'''
Calculates the distance between a fields_array and a point
'''

def calculate_distance(fields_arr, point, eig_fractions_inverted):
	distance = 0
	for index in range(len(fields_arr)):
		field = fields_arr[index]
		center_field = point.center[index]
		eig_inverted = eig_fractions_inverted[index]
		distance += ((field - center_field)**2) * eig_inverted
	distance = math.sqrt(distance)
	return distance


'''
Finds the closest neighbor, uses eig_fractions to weigh the distances
'''
def find_closest_neighbor(fields_arr, list_of_points, eig_fractions):
	eig_fractions_inverted = map(invert, eig_fractions)
	closest_point = None
	min_distance = 1000000000
	for point in list_of_points:
		distance = calculate_distance(fields_arr, point, eig_fractions_inverted)
		if distance < min_distance:
			min_distance = distance
			closest_point = point
	return closest_point

'''
MC for N points
'''

def generate_samples_get_breach_prob(number_of_samples, list_of_points, list_of_list_of_bins, probs_of_bins_for_each_field, eig_fractions):
	count_of_breach = 0
	for number in range(number_of_samples):
		this_sample = generate_a_sample(list_of_list_of_bins, probs_of_bins_for_each_field)
		closest_neighbor = find_closest_neighbor(this_sample, list_of_points, eig_fractions)
		prob_of_breach = closest_neighbor.probability(this_sample)
		prob_of_breach *= 100
		print "PROB OF BREACH: ", prob_of_breach
		random.seed()
		rand_numb = random.randrange(0, 100)
		if rand_numb <= prob_of_breach:
			count_of_breach += 1

	print "COUNT OF BREACH: ", count_of_breach
	return (float(count_of_breach) / float(number_of_samples))