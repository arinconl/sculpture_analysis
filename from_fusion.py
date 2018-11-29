"""
Serves to parse data from Fusion 360 data.out files.
"""



def read_fusion_file(file_name):
#!TODO: Clean this code up (considered too long stylistically), also poorly documented! (It is a bit hard to follow for what 'simple' of a task it's fulfilling...)

	f = open(file_name, "r")

	line = ""
	
	# Note: this seems to be 360 on PCs, 361 on Macs
	# start_line = 361

	header_buf = 350

	for _ in range(header_buf):
		line = f.readline()

	data = []
	data_row = []
	curr = ""
	jj = 0
	kk = False

	while (len(line) > 0 ):
		f.readline()
		if "MODE" in line:
			break
	
	while (len(line) > 3):
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
