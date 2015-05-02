# -*- coding:utf-8 -*-
from myfile import *
from setting import *

class SpdexMatchInfo:
	"""
	20150501,001,aaa,bbb,2015/5/1 17:30,27431148
	"""
	def __init__(self,match_id,home_name,away_name,match_time,tid):
		self.match_id = match_id
		self.home_name = home_name
		self.away_name = away_name
		self.match_time = match_time
		self.tid = tid
		#print type(match_id),type(home_name),type(away_name),type(match_time),type(tid)
		#unicode,unicode,unicode,datetime.datetime,unicode

	def unicode(self):
		return u"{0},{1} VS {2},{3},{4}".format(self.match_id,self.home_name,self.away_name,self.match_time,self.tid)

class BetfairMatchInfo_1X2:

	def __init__(self,match_id,market_id,home_id,away_id,draw_id,home_eng_name,away_eng_name):
		self.match_id = match_id
		self.market_id = market_id
		self.home_id = home_id
		self.away_id = away_id
		self.draw_id = draw_id
		self.home_eng_name = home_eng_name
		self.away_eng_name = away_eng_name

		self.charts = BetfairCharts_1X2(self)

	def unicode(self):
		return "{0}-{1},{2},{3},{4},{5}".format(self.home_eng_name,self.away_eng_name,self.market_id,self.home_id,self.away_id,self.draw_id)

	def get_home_chart_url(self,log):
		url = url_betfair_chart_fmt.format(self.market_id,self.home_id,log)
		return url
	def get_away_chart_url(self,log):
		url = url_betfair_chart_fmt.format(self.market_id,self.away_id,log)
		return url
	def get_draw_chart_url(self,log):
		url = url_betfair_chart_fmt.format(self.market_id,self.draw_id,log)
		return url

	def save_charts(self,root_dir):
		overwrite = IMAGE_OVERWRITE
		myfile = MyFile()
		url_path_mapping = [
			(self.charts.url_odd_home,root_dir+self.charts.file_odd_home),
			(self.charts.url_odd_away,root_dir+self.charts.file_odd_away),
			(self.charts.url_odd_draw,root_dir+self.charts.file_odd_draw),
			(self.charts.url_prob_home,root_dir+self.charts.file_prob_home),
			(self.charts.url_prob_away,root_dir+self.charts.file_prob_away),
			(self.charts.url_prob_draw,root_dir+self.charts.file_prob_draw)
		]
		for (url,filepath) in url_path_mapping:
			myfile.download_image(url,filepath,overwrite)


class BetfairMatchInfo_OverUnder:

	def __init__(self,match_id,market_id,over_id,under_id,over_name,under_name):
		self.match_id = match_id
		self.market_id = market_id
		self.over_id = over_id
		self.under_id = under_id
		self.over_name = over_name
		self.under_name = under_name

		self.charts = BetfairCharts_OverUnder(self)

	def unicode(self):
		return "{0}-{1},{2},{3},{4}".format(self.over_name,self.under_name,self.market_id,self.over_id,self.under_id)

	def get_over_chart_url(self,log):
		url = url_betfair_chart_fmt.format(self.market_id,self.over_id,log)
		return url
	def get_under_chart_url(self,log):
		url = url_betfair_chart_fmt.format(self.market_id,self.under_id,log)
		return url

	def save_charts(self,root_dir):
		# charts/jc/20150501/  charts/m14/15068/
		overwrite = IMAGE_OVERWRITE
		myfile = MyFile()
		url_path_mapping = [
			(self.charts.url_odd_over,root_dir+self.charts.file_odd_over),
			(self.charts.url_odd_under,root_dir+self.charts.file_odd_under),
			(self.charts.url_prob_over,root_dir+self.charts.file_prob_over),
			(self.charts.url_prob_under,root_dir+self.charts.file_prob_under)
		]
		for (url,filepath) in url_path_mapping:
			myfile.download_image(url,filepath,overwrite)

class BetfairCharts_1X2:

	def __init__(self,betfair_1x2):
		match_id = betfair_1x2.match_id
		# url odd
		self.url_odd_home = betfair_1x2.get_home_chart_url(False)
		self.url_odd_away = betfair_1x2.get_away_chart_url(False)
		self.url_odd_draw = betfair_1x2.get_draw_chart_url(False)
		# url prob
		self.url_prob_home = betfair_1x2.get_home_chart_url(True)
		self.url_prob_away = betfair_1x2.get_away_chart_url(True)
		self.url_prob_draw = betfair_1x2.get_draw_chart_url(True)

		# file odd
		self.file_odd_home = "{0}_{1}".format(match_id,"odd_home.jpg")
		self.file_odd_away = "{0}_{1}".format(match_id,"odd_away.jpg")
		self.file_odd_draw = "{0}_{1}".format(match_id,"odd_draw.jpg")
		# file prob
		self.file_prob_home = "{0}_{1}".format(match_id,"prob_home.jpg")
		self.file_prob_away = "{0}_{1}".format(match_id,"prob_away.jpg")
		self.file_prob_draw = "{0}_{1}".format(match_id,"prob_draw.jpg")

class BetfairCharts_OverUnder:

	def __init__(self,betfair_overunder):
		match_id = betfair_overunder.match_id
		# url odd
		self.url_odd_over = betfair_overunder.get_over_chart_url(False)
		self.url_odd_under = betfair_overunder.get_under_chart_url(False)
		# url prob
		self.url_prob_over = betfair_overunder.get_over_chart_url(True)
		self.url_prob_under = betfair_overunder.get_under_chart_url(True)

		# file odd
		self.file_odd_over = "{0}_{1}".format(match_id,"odd_over.jpg")
		self.file_odd_under = "{0}_{1}".format(match_id,"odd_under.jpg")
		# file prob
		self.file_prob_over = "{0}_{1}".format(match_id,"prob_over.jpg")
		self.file_prob_under = "{0}_{1}".format(match_id,"prob_under.jpg")

class MatchInfo:

	def __init__(self,match_type,sid,spdex,betfair_1x2,betfair_overunder):
		self.match_type = match_type
		self.sid = sid
		self.spdex = spdex
		self.betfair_1x2 = betfair_1x2
		self.betfair_overunder = betfair_overunder

	def get_spdex(self):
		return self.spdex

	def get_betfair_1x2(self):
		return self.betfair_1x2

	def get_betfair_overunder(self):
		return self.betfair_overunder

	def unicode(self):
		u1 = u""
		u2 = u"Betfair market has closed!"
		u3 = u"Betfair market has closed!"
		if self.spdex:
			u1 = self.spdex.unicode()
		if self.betfair_1x2:
			u2 = self.betfair_1x2.unicode()
		if self.betfair_overunder:
			u3 = self.betfair_overunder.unicode()
		return u"{0}\n{1}\n{2}".format(u1,u2,u3)

	def save_charts(self):
		root_dir = get_match_chart_root_dir(self.match_type,self.sid)
		if self.betfair_1x2:
			self.betfair_1x2.save_charts(root_dir)
		if self.betfair_overunder:
			self.betfair_overunder.save_charts(root_dir)

def get_match_chart_root_dir(match_type,sid):
	# ./charts/jc/    20150501
	# ./charts/m14/    15067
	root_dir = GDATA[match_type].get("ROOT_DIR")+sid+"/"
	return root_dir

class MatchCollectionBydate:

	def __init__(self,id):
		self.id = id
		self.match_list = []

	def add_match(self,match):
		self.match_list.append(match)

	def add_match_list(self,match_list):
		for match in match_list:
			self.add_match(match)

	def get_match_list(self):
		return self.match_list

	def match_count(self):
		return len(self.match_list)
