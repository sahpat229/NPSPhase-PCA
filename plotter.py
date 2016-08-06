import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from dict_establish import Point
from cycler import cycler


"""
list_of_points is the list of Points generated from dist_establish
(i.e., the probability distribution).  Fineness determines the number
of points to generate in the evenly spaced interval
"""

def plot_distribution(list_of_points, fineness):
	initial_point = list_of_points[0]
	end_range_of_center = len(initial_point.center)

	plt.rc('lines', linewidth=4)
	plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +
		cycler('linestyle', ['-', '--', ':', '-.'])))

	fig, axes = plt.subplots(nrows=end_range_of_center)

	min = 10000000000
	max = -10000000000
	for component_index in range(end_range_of_center):

		list_of_list_of_xcoords = []
		list_of_list_of_ycoords = []
		current_ax = axes[component_index]
		current_ax.set_ylim(0.00, 1.00)

		for point in list_of_points:
			
			left_influence_side = point.center[component_index] - (2*point.influence_region_radii[component_index])
			right_influence_side = point.center[component_index] + (2*point.influence_region_radii[component_index])
			if (left_influence_side < min):
				min = left_influence_side
			if (right_influence_side > max):
				max = right_influence_side
			list_of_xcoords = np.linspace(left_influence_side, right_influence_side, fineness)
			list_of_ycoords = [point.probability_component(component_index, x) for x in list_of_xcoords]
			list_of_list_of_xcoords.append(list_of_xcoords)
			list_of_list_of_ycoords.append(list_of_ycoords)

		print "MIN:", min, "MAX:", max
		current_ax.set_xlim(min, max)
		for (this_list_of_xcoords, this_list_of_ycoords) in zip(list_of_list_of_xcoords, list_of_list_of_ycoords):
			current_ax.plot(this_list_of_xcoords, this_list_of_ycoords)

		current_ax.set_title(str(component_index))


	plt.subplots_adjust(hspace=0.3)
	plt.show()