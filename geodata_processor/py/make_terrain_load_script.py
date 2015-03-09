"""
usage:
make_terrain_load_script.py region_name_prefix terrain_filename_prefix xmax ymax
For example, "make_terrain_load_script.py huyu v_ 3 6" will generate a file named terrain_load_script.txt.
"""

import sys

output_filename = "terrain_load_script.txt" 

def make_script(region_pre, terrain_pre, xmax, ymax):
	f = open(output_filename, "w")
	for x in range(xmax+1):
		for y in range(ymax+1):
			f.write("change region " + region_pre + str(x) + str(y) + "\n")
			f.write("terrain load " + terrain_pre  + str(x) + str(y) + ".r32\n")
	f.close()

if __name__ == "__main__":
	if len(sys.argv) != 5:
		print __doc__
	else:
		region_name_prefix = sys.argv[1]
		terrain_filename_prefix = sys.argv[2]
		xmax = int(sys.argv[3])
		ymax = int(sys.argv[4])
		make_script(region_name_prefix, terrain_filename_prefix, xmax, ymax)
		print output_filename, "has been made!"
