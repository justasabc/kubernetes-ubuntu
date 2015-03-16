import json

def dict_to_json():
	d = {}
	d['id'] = 'sim1-pod'
	d['kind'] = 'Pod'
	d['apiVersion'] = 'v1beta1'
	with open('result.json', 'w') as fp:
    		json.dump(d, fp, indent=2, separators=(',', ':'))

def json_to_dict():
	with open('result.json', 'r') as fp:
    		d = json.load(fp)
		print d
def test():
	dict_to_json()
	json_to_dict()
	print "OK"

def main():
	test()

if __name__=="__main__":
	main()
