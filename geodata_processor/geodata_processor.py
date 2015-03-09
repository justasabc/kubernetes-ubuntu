from osgeo import ogr
from osgeo import gdal
import numpy
import sys
import struct

regionWidth = 256
regionHeight = 256
resolution = 32

def coord_geo2img(xyTuple, dem):
	"""
	GDAL transformation: from georeference coordinates to image coordinates
	Refer to "Affine GeoTransform" in http://www.gdal.org/gdal_datamodel.html
	"""
	geotransform = dem.GetGeoTransform()
	x = (xyTuple[0] - geotransform[0]) / geotransform[1]
	y = (xyTuple[1] - geotransform[3]) / geotransform[5]
	#image coordinates need to be int
	return (int(x), int(y))

def get_boundary_points(feature):
	bound = feature.GetGeometryRef().GetBoundary()
	#print bound  # linestring
	xs = map(bound.GetX, (0, 1, 2))
	ys = map(bound.GetY, (0, 1, 2))
	xLeft = min(xs)
	yBottom = min(ys)
	xRight = max(xs)
	yTop = max(ys)
	#in function make_r32, I use only leftTop and rightBottom
	return {"leftBottom":(xLeft, yBottom), "rightTop":(xRight, yTop), \
			"leftTop":(xLeft, yTop), "rightBottom":(xRight, yBottom)}

def interpolate(array_2d):
	"""
	array_2d is a (256+32*2)*(256+32*2) 2-dimentional array of numpy. This function use bilinear method to interpolate the array.
	The precision of the array is 32*32, which implies there are (8+2)*(8+2)=100 kinds of values in the array.
	For example, all elements of array_2d[0:32, 0:32] have the same value, and array_2d[16,16] is treated as the basis point of this 32*32 block. 
	For any element except marginal elements 16 away from any border, it uses 4 nearest basis points to interpolate its value.
	"""
	#range(16, 256+32, 32)
	#16 deals with the start, 256+32 deals with the end, 32 is the step
	for x in range(resolution>>2, regionWidth+resolution, resolution): 
		for y in range(resolution>>2, regionHeight+resolution, resolution):	#as above
			#lb:leftbottom, rb:rightbottom, lt:lefttop, rt:righttop
			#in fact, the coordinate system is left-top coordinate system, 
			#so bigger y is below smaller y, but I don't want to modify the variables' names anymore
			lb = array_2d[x, y]
			rb = array_2d[x+resolution, y]
			lt = array_2d[x, y+resolution]
			rt = array_2d[x+resolution, y+resolution]
			for xx in range(x, x+resolution):
				for yy in range(y, y+resolution):
					tx = (xx - x) / float(resolution)
					ty = (yy - y) / float(resolution)
					array_2d[xx, yy] = (1-tx) * ((1-ty)*lb + ty*lt) + tx * ((1-ty)*rb + ty*rt) 

def make_r32(region_prefix,shpfile_path, dem_path,out_folder):
	"""
	region_prefix: huyu,xwd
	"""	
	driver = ogr.GetDriverByName('ESRI Shapefile')
	shpfile = driver.Open(shpfile_path)
	dem = gdal.Open(dem_path)

	band = dem.GetRasterBand(1)
	layer = shpfile.GetLayer(0)		
	featureCount = layer.GetFeatureCount()
	# featureCount = 5 # added by kzl
	for i in range(featureCount):
		feature = layer.GetFeature(i)
		#there are 4 fields: id,x,y,name
		x = feature.GetField(1)	
		y = feature.GetField(2)	
		if x == None:
			x = 0
		if y == None:
			y = 0
		regionName = "{0}_{1}{2}".format(region_prefix,x,y)

		boundaryPoints_geo = get_boundary_points(feature)	#geo coordinate
		#transform coord from geo to img
		leftTop_img = coord_geo2img(boundaryPoints_geo["leftTop"], dem)
		rightBottom_img = coord_geo2img(boundaryPoints_geo["rightBottom"], dem)

		# set params for ReadRaster
		xoff = leftTop_img[0] -1 
		yoff = leftTop_img[1] -1
		xsize = rightBottom_img[0] - leftTop_img[0] +2 
		ysize = rightBottom_img[1] - leftTop_img[1] +2
		buf_xsize = regionWidth + resolution*2 # 320
		buf_ysize = regionHeight + resolution*2 # 320
		datatype = band.DataType  
		data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}  
		type_struct = data_types[gdal.GetDataTypeName(datatype)]
		#print xoff,yoff,xsize,ysize
		
    		bufferStr = band.ReadRaster(xoff,yoff,xsize,ysize,buf_xsize,buf_ysize,datatype)
    		bufferArray = struct.unpack(type_struct *buf_xsize * buf_ysize, bufferStr)
		buffer2d = numpy.array(bufferArray).reshape(buf_xsize, buf_ysize)

		# interpolate data to upgrade from 30m to 1m
		interpolate(buffer2d)

		#remove buffer
		noBuffer = numpy.vsplit(numpy.hsplit(buffer2d, (resolution, resolution + regionWidth))[1], (resolution, resolution + regionHeight))[1]
		#.r32 file records heightfield from west to east, then from south to north
		r32 = numpy.zeros((regionHeight, regionWidth), dtype=numpy.float32)
		for j in range(regionHeight):
			r32[j] = noBuffer[regionHeight - 1 - j]
		outfile_path = "{0}{1}{2}".format(out_folder,regionName,".r32")
		r32.tofile(outfile_path)
		print outfile_path + " generated!"
	shpfile = None
	dem = None
	print "Success!"

def run_make_r32_huyu():
	region_prefix = "huyu"
	shpfile_path = './huyu/huyu_grid_74.shp'
	dem_path = './huyu/huyu_dem.tif'
	out_folder = './output/r32/'
	make_r32(region_prefix,shpfile_path,dem_path,out_folder)

def run_make_r32_xwd():
	region_prefix = "xwd"
	shpfile_path = './xwd/xwd_grid_75.shp'
	dem_path = './xwd/xwd_dem.tif'
	out_folder = './output/r32/'
	make_r32(region_prefix,shpfile_path,dem_path,out_folder)

#gdal_translate -projwin 416200.574337 4428986.45863 416456.191082 4428730.47089 -of GTiff Z:/xwd/data/1_image/xwd/proj_xwd.tif Z:/xwd/data/1_image/xwd/clip_image/test.clip
# EPSG:3857 - WGS 84 / Pseudo Mercator

def make_script_clip_image_by_shape(region_prefix,image_file,shape_file,command_file,out_folder,out_ext):
	"""
	region_prefix: huyu,xwd
	out_ext:  .png, .tif
	"""	
	# of: output format  GTiff PNG JPEG
	command_str = "gdal_translate -projwin %s %s %s %s -of JPEG %s %s"
	driver = ogr.GetDriverByName('ESRI Shapefile')
	shpfile = driver.Open(shape_file)
	f = open(command_file,'w')

	layer = shpfile.GetLayer(0)		
	featureCount = layer.GetFeatureCount()
	print featureCount
	#featureCount =  1# added by kzl
	for i in range(featureCount):
		feature = layer.GetFeature(i)
		#there are 4 fields: id,x,y,name
		x = feature.GetField(1)	
		y = feature.GetField(2)	
		if x == None:
			x = 0
		if y == None:
			y = 0
		print x,y
		regionName = "{0}{1}{2}".format(region_prefix,x,y)
		boundaryPoints_geo = get_boundary_points(feature)
		lt = boundaryPoints_geo['leftTop']
		rb = boundaryPoints_geo['rightBottom']
		tile_file = "{0}{1}{2}".format(out_folder,regionName,out_ext)
		line = command_str % (lt[0],lt[1],rb[0],rb[1],image_file,tile_file)
		f.write(line+'\n')
	f.close()
	print command_file + " generated!"
	shpfile = None
	print "Finished!"

# Using ArcGIS to export xwd.tif from 16bit to 8bit
def run_clip_image_xwd():
	region_prefix = "xwd"
	image_file = './data/proj_xwd.tif'
	shape_file = './data/xwd/xwd_grid_75.shp'
	command_file = 'clip_image_script_xwd.txt'
	out_folder = './output/jpg/'
	out_ext = '.jpg'
	make_script_clip_image_by_shape(region_prefix,image_file,shape_file,command_file,out_folder,out_ext)

def run_clip_image_huyu():
	region_prefix = "huyu"
	image_file = './data/proj_huyu.tif'
	shape_file = './data/huyu/huyu_grid_74.shp'
	command_file = 'clip_image_script_huyu.txt'
	out_folder = './output/jpg/'
	out_ext = '.jpg'
	make_script_clip_image_by_shape(region_prefix,image_file,shape_file,command_file,out_folder,out_ext)

def main():
	#run_make_r32_huyu()
	#run_make_r32_xwd()
	#run_clip_image_huyu()
	run_clip_image_xwd()

if __name__ == "__main__":
	main()
