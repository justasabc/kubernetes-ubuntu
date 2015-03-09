"""
Make script for loading all regions' oars
usage:
make_load_oar_script.py region_name_prefix xmax ymax
For example, "make_load_oar_script.py xwd 5 7 | huyu 4 7" will generate a file named load_all_oar_script.txt.
"""

import sys

output_filename = "load_all_oar_script.txt" 

def make_script(region_pre, xmax, ymax):
	f = open(output_filename, "w")
	for y in range(ymax):
		for x in range(xmax):
			f.write("change region " + region_pre + str(x) + str(y) + "\n")
			f.write("load oar " + region_pre  + str(x) + str(y) + ".oar\n")
	f.close()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print __doc__
	else:
		region_name_prefix = sys.argv[1]
		xmax = int(sys.argv[2])
		ymax = int(sys.argv[3])
		make_script(region_name_prefix, xmax, ymax)
		print output_filename, "has been made!"
