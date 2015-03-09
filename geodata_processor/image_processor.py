import Image

def resize_image(infilepath,outfilepath,width,height):
	print infilepath
	img = Image.open(infilepath)
	imgnew = img.resize((width,height),Image.ANTIALIAS)
	imgnew.save(outfilepath)
	print outfilepath+" generated!"

def batch_resize(region_prefix,rx,ry,in_folder,out_folder,in_ext,out_ext,width,height):
	for x in range(rx):
		for y in range(ry):
			filename = "{0}{1}{2}".format(region_prefix,x,y)
			infilepath = in_folder + filename + in_ext
			outfilepath = out_folder + filename + out_ext
			resize_image(infilepath,outfilepath,width,height)
	print "Finished!"

def run_batch_resize_huyu():
	region_prefix = 'huyu'
	rx = 4 
	ry = 7
	in_folder = './output/jpg/' 
	out_folder = './output/jpg/'
	in_ext ='.jpg'
	out_ext ='.jpg'
	width = 1024
	height = 1024
	batch_resize(region_prefix,rx,ry,in_folder,out_folder,in_ext,out_ext,width,height)
	
def run_batch_resize_xwd():
	region_prefix = 'xwd'
	rx = 5 
	ry = 7
	in_folder = './output/jpg/' 
	out_folder = './output/jpg/'
	in_ext ='.jpg'
	out_ext ='.jpg'
	width = 1024
	height = 1024
	batch_resize(region_prefix,rx,ry,in_folder,out_folder,in_ext,out_ext,width,height)

def main():
	#run_batch_resize_huyu()
	run_batch_resize_xwd()

if __name__=="__main__":
	main()
