"""
usage:
make_region_ini.py prefix xmax ymax
xmax and ymax have to be 1 digit non-negative number.
For example, "make_region_ini.py v 3 2" will create v00.ini, v01.ini, ..., v02.ini, v10.ini, ..., v12.ini, ..., v32.ini
"""

import sys
import uuid

def make_region_ini(prefix, x, y):
	regionName = prefix + str(x) + str(y)
	f = open(prefix + str(x) + str(y) + ".ini", "w")
	f.write("[" + regionName + "]\n")
	f.write("RegionUUID = " + str(uuid.uuid1()) + "\n")
	f.write("Location = " + str(1000 + x) + "," + str(1000 + y) + "\n")
	f.write("InternalAddress = 0.0.0.0\n")
	f.write("InternalPort = " + str(9000 + 10*x + y) + "\n")
	f.write("AllowAlternatePorts = False\n")
	f.write("ExternalHostName = SYSTEMIP\n")
	f.close()
	print prefix + str(x) + str(y) + ".ini generated"

def make_inis(prefix, xmax, ymax):
	for x in range(xmax+1):
		for y in range(ymax+1):
			make_region_ini(prefix, x, y)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print __doc__
	prefix = sys.argv[1]
	xmax = int(sys.argv[2])
	ymax = int(sys.argv[3])
	make_inis(prefix, xmax, ymax)
	print "Success!"
