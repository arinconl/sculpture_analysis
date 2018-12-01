"""
Serves to parse data from Fusion 360 data.out files.

!TODO:
- Account for separated frequencies (0-60, 61-120, 121-180)
"""



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
