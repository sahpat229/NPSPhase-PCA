from dict_establish import Point
from bin_establish import Bin
import random

'''
Takes a list_of_list_of_bins generated by bin_establish and a total_counts list generated by
bin_establish, and generates the probability for picking a bin, (i.e., the first "roll") for each
field
'''


def sampling_for_which_bin(list_of_list_of_bins, total_counts):
	probs_of_bins_for_each_field = []
	for list_of_bins in list_of_list_of_bins, total_count in total_counts:
		probs_for_this_field = []
		for bin in list_of_bins:
			probs_for_this_field.append(float(bin.count) / float(total_count))
		probs_of_bins_for_each_field.append(probs_for_this_field)

	return probs_of_bins_for_each_field

def generate_a_sample(list_of_list_of_bins, probs_of_bins_for_each_field):
	random.seed()

	fields_arr = []

	for list_of_bins in list_of_bins, probs_for_this_field in probs_of_bins_for_each_field:
		random_numb = random.randrange(0, 100)
		random_numb /= 100
		for index in range(0, len(probs_for_this_field)):
			random_numb -= probs_for_this_field[index]
			if random_numb <= 0:
				selected_bin = list_of_bins[index]
				fields_arr.append(selected_bin.random_sample())
				
	return fields_arr