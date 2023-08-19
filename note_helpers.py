"""
filter through list of notes

check if "x" notes are in there

(so we don't have to do this analysis by hand)
"""



import math
import statistics
import numpy as np



def extract_midi_values(all_notes):

	midis = []

	for n in all_notes:
		midis.append(n.midi)
	
	return np.array(midis)

def compare_with_pd(midis):

	pd_midis = np.array([
		65.1001, 
		78.8999, 
		86.0998, 
		87.8998, 
		88.1998, 
		89.0998, 
		89.1998, 
		89.6998, 
		89.9998, 
		90.1998, 
		90.9997, 
		91.3997, 
		92.9997, 
		93.8997, 
		94.1997, 
		94.6997, 
		96.7997, 
		97.4996, 
		97.5996, 
		100.8, 
		101.1, 
		101.3, 
		101.6, 
		102.2, 
		102.6, 
		105, 
		105.4, 
		106.5, 
		107.499, 
		108.199, 
		109.499, 
		110.899, 
		111.599, 
		111.999, 
		112.299, 
		112.499, 
		113.199, 
		113.499, 
		113.599, 
		113.799, 
		114.199, 
		118.499, 
		118.899, 
		119.399, 
		119.499, 
		119.999
	])

	num_notes_pd = pd_midis.size
	num_notes_fusion = midis.size

	print("Fusion has " + str(num_notes_fusion) + " notes.")
	print("PureData has " + str(num_notes_pd) + " notes.")

	# print(midis)
	# print(pd_midis)

	"""
	pd_bounds = []
	# Generate list of bounds
	for n in pd_midis:
		pd_bounds.append(math.floor(n))
	"""
	pd_bounds_h = gen_iter_bounds(pd_midis)
	pd_bounds_l_l, pd_bounds_l_u = gen_iter_bounds2(pd_midis)

	# print(pd_bounds_l_l)
	# print(pd_bounds_l_u)

	# Prune to only values that could be present
	midis = prune_for_potentials(midis, pd_bounds_l_l, pd_bounds_l_u)

	print(midis)
	print(pd_midis)
	
	# Try and compare!
	midis, diffs = prune_to_present(midis, pd_midis)

	print("On average, note difference of " + str(statistics.mean(diffs)))
	

def gen_iter_bounds(pd):

	hsh = {}

	for n in pd:
		t = math.floor(n)
		if t in hsh:
			hsh[t] += 1
		else:
			hsh[t] = 1
	
	return hsh

def gen_iter_bounds2(pd):

	lst_l = []
	lst_u = []

	for n in pd:
		if math.floor(n) not in lst_l:
			lst_l.append(math.floor(n))
			lst_u.append(math.ceil(n))
	
	return lst_l, lst_u

def prune_for_potentials(midis, bounds_l, bounds_u):

	pruned_list = []

	c = 0

	for n in midis:
		if (math.floor(n) in bounds_l) and (math.ceil(n) in bounds_u):
			c += 1
			pruned_list.append(n)
	
	print("There are " + str(c) + " notes that may correspond to the measured!")

	return np.array(pruned_list)

	"""
	for n in midis:
		curr_bound = min(bounds.keys(), key=(lambda k: bounds[k]))

		if curr_bound < n < (curr_bound + 1):
			pruned_list.append(n)
			c += 1
			bounds[curr_bound] -= 1

			if bounds[curr_bound] <= 0:
				bounds.pop(curr_bound)
	"""

def prune_to_present(theo, expr):
	
	lst_t = []
	lst_e_l = []
	lst_e_u = []
	lst_o = []
	lst_d = []

	c = 0

	for n in theo:
		lst_t.append(round(n,1))
	
	for n in expr:
		lst_e_l.append(math.floor(10*n)/10)
		lst_e_u.append(math.ceil(10*n)/10)
	
	for n in range(len(lst_t)):
		if (lst_t[n] in lst_e_l) or (lst_t[n] in lst_e_u):
			c += 1
			lst_o.append(theo[n])

			if lst_t[n] in lst_e_l:
				print(str(theo[n]) + " corresponds to " + str(expr[lst_e_l.index(lst_t[n])]), end="")
				lst_d.append(abs(theo[n] - expr[lst_e_l.index(lst_t[n])]))
			else:
				print(str(theo[n]) + " corresponds to " + str(expr[lst_e_u.index(lst_t[n])]), end="")
				lst_d.append(abs(expr[lst_e_u.index(lst_t[n])] - theo[n]))
			
			print(" with a difference of " + str(round(lst_d[-1], 4)))
	
	print("There are " + str(c) + " notes that correspond to measured!")

	return lst_o, lst_d



