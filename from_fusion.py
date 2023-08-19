"""
Serves to parse data from Fusion 360 data.out files.

!TODO:
- Account for separated frequencies (0-60, 61-120, 121-180)
"""


import numpy as np


def extract_from_collection():

	#
	# Ask user for files
	#

	file_names = []
	while True:
		
		file_name_curr = input("Enter an input file (type \"Q\" to finish): ")

		if (file_name_curr[0] == "Q"):
			break
		elif (len(file_name_curr) > 0):
			file_names.append(file_name_curr)
		else:
			break

	print("Collected files: ")
	file_names = [
		"inputs/fusion20-1000.out", "inputs/fusion1000-2000.out", 
		"inputs/fusion2000-3000.out", "inputs/fusion3000-4000.out", 
		"inputs/fusion4000-5000.out", "inputs/fusion5000-6000.out", 
		"inputs/fusion6000-7000.out", "inputs/fusion7000-8000.out", 
		"inputs/fusion8000-9000.out", "inputs/fusion9000-10000.out", 
		]
	print(file_names)
	print()
	

	#
	# Extract notes in files
	#

	if len(file_names) > 1:
		data = np.array(read_fusion_file(file_names[0]))
		file_names.reverse()
		file_names.pop()
		file_names.reverse()

		for f in file_names:
			data = np.vstack((data, read_fusion_file(f)))

	elif len(file_names) == 1:
		data = np.array(read_fusion_file(file_names[0]))

	else:
		data = np.array([])

	# Process our data

	# Sort it (wrt/ radian row)
	data[data[:,1].argsort()]

	# Remove dupes
	# new_array = [tuple(row) for row in data]
	# pruned = np.unique(new_array)

	# print(data)
	# print()
	# print(pruned)


	return data

def set_fusion_data():
	# ask for files to use

	# get data for each
	# np.vstack at each iteration
	data = 2

	return data

def read_fusion_file(file_name):
#!TODO: Clean this code up! It is a bit hard to follow for what 'simple' of a task it's fulfilling...

	# Open our file for reading
	f = open(file_name, "r")

	# Note: this seems to be 360 on PCs, 361 on Macs
	# start_line = 361
	header_buf = 350

	line = ""
	for _ in range(header_buf):
		line = f.readline()

	data = []
	data_row = []
	curr = ""
	jj = 0
	kk = False

	in_mode_section = True

	while (in_mode_section):
		while (True):
			line = f.readline()
			if len(line) and ("R E A L   E I G E N V A L U E S" in line):
				line = f.readline()
				line = f.readline()
				line = f.readline()
				line = f.readline()
				break
			elif len(line) and ("M O D A L   P A R T I C I P A T I O N   F A C T O R S" in line):
				in_mode_section = False
				break
		
		if (in_mode_section):
			while (len(line) > 4):
				for ch in line:
					if ( ( ch != ' ') and (ch != '\n') ):
						curr += ch
						if (kk == False):
							kk = True
					elif (kk):
						if (jj == 0):
							data_row.append(int(curr))
						else:
							data_row.append(float(curr))
						
						jj += 1

						curr = ""
						kk = False

				data.append(data_row)
				data_row = []
				jj = 0

				# Get next line and loop
				line = f.readline()

	return data

def print_fusion_data(fusion_data):
	"""
	Prints out the contents of the fusion frequency data var.
	"""
	print("[")
	for ln in fusion_data:
		print(ln)
	print("]")


def get_data_rads(data):
	rads = []

	for ii in range(len(data)):
		rads.append(data[ii][2])
	
	return rads
