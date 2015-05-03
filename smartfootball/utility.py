from datetime import datetime

def pad_seq(seq):
	fmt = u'%03d'
	return fmt % seq

def pad_day(d):
	fmt = u'%02d'
	return fmt % d

def get_today_sid_jc():
	# 20150501
	now = datetime.now()
	sid = "{0}{1}{2}".format(now.year,pad_day(now.month),pad_day(now.day))
	return sid

