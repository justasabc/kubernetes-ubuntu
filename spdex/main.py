# -*- coding:utf-8 -*-
import requests
import lxml.html 
from datetime import datetime
import time
from myfile import *

url_m14 = "http://c.spdex.com/spdex500a"
url_jc = "http://c.spdex.com/spdex500b"
url_viewerqq_fmt = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id={0}"
url_betfair_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
url_betfair_chart_fmt = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId={0}&selectionId={1}&logarithmic={2}"

# page_count
# jcid
# VIEWSTATE
def get_params_jc(url):
	#print r.encoding # utf-8
	#print type(r.text) # unicode
	#html element methods
	#http://lxml.de/lxmlhtml.html#html-element-methods
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	# 1) page_count
	page_select = html.xpath('//*[@id="AspNetPager1_input"]')[0]
	page_options = page_select.getchildren()
	page_count = len(page_options)
	# 2) jcid
	jcid_select = html.xpath('//*[@id="DropJcId"]')[0]
	jcid = unicode(jcid_select.findtext('option'))
	# 3) viewstate
	viewstate_input = html.xpath('//*[@id="__VIEWSTATE"]')[0]
	viewstate = viewstate_input.attrib['value']
	return page_count,jcid,viewstate

def get_params_m14(url):
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	# 1) m14id
	# //*[@id="DropLotteryId"]/option[1]
	m14id_select = html.xpath('//*[@id="DropLotteryId"]')[0]
	m14id = unicode(m14id_select.findtext('option'))
	# 2) viewstate
	viewstate_input = html.xpath('//*[@id="__VIEWSTATE"]')[0]
	viewstate = viewstate_input.attrib['value']
	return m14id,viewstate

"""
__EVENTTARGET:AspNetPager1
__EVENTARGUMENT:2
__LASTFOCUS:
__VIEWSTATE: 
DropJcId:20150430
AspNetPager1_input:2
"""
def get_post_payload(jcid,page,viewstate):
	payload = {}
	payload['__EVENTTARGET'] = 'AspNetPager1'
	payload['__EVENTARGUMENT'] = page
	payload['__LASTFOCUS'] = None
	payload['__VIEWSTATE'] = viewstate
	payload['DropJcId'] = jcid
	payload['AspNetPager1_input'] = page
	return payload

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

	def save_charts(self):
		overwrite = False
		myfile = MyFile()
		url_path_mapping = [
			(self.charts.url_odd_home,self.charts.file_odd_home),
			(self.charts.url_odd_away,self.charts.file_odd_away),
			(self.charts.url_odd_draw,self.charts.file_odd_draw),
			(self.charts.url_prob_home,self.charts.file_prob_home),
			(self.charts.url_prob_away,self.charts.file_prob_away),
			(self.charts.url_prob_draw,self.charts.file_prob_draw)
		]
		for (url,filepath) in url_path_mapping:
			myfile.download_image(url,filepath,overwrite)

class BetfairCharts_1X2:

	def __init__(self,betfair_1x2):
		self.betfair_1x2 = betfair_1x2
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
		self.file_odd_home = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"odd_home.jpg")
		self.file_odd_away = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"odd_away.jpg")
		self.file_odd_draw = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"odd_draw.jpg")
		# file prob
		self.file_prob_home = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"prob_home.jpg")
		self.file_prob_away = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"prob_away.jpg")
		self.file_prob_draw = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"prob_draw.jpg")

class BetfairCharts_OverUnder:

	def __init__(self,betfair_overunder):
		self.betfair_overunder = betfair_overunder
		match_id = betfair_overunder.match_id
		# url odd
		self.url_odd_over = betfair_overunder.get_over_chart_url(False)
		self.url_odd_under = betfair_overunder.get_under_chart_url(False)
		# url prob
		self.url_prob_over = betfair_overunder.get_over_chart_url(True)
		self.url_prob_under = betfair_overunder.get_under_chart_url(True)

		# file odd
		self.file_odd_over = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"odd_over.jpg")
		self.file_odd_under = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"odd_under.jpg")
		# file prob
		self.file_prob_over = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"prob_over.jpg")
		self.file_prob_under = "{0}/{1}_{2}".format(ROOT_DIR,match_id,"prob_under.jpg")

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

	def save_charts(self):
		overwrite = False
		myfile = MyFile()
		url_path_mapping = [
			(self.charts.url_odd_over,self.charts.file_odd_over),
			(self.charts.url_odd_under,self.charts.file_odd_under),
			(self.charts.url_prob_over,self.charts.file_prob_over),
			(self.charts.url_prob_under,self.charts.file_prob_under)
		]
		for (url,filepath) in url_path_mapping:
			myfile.download_image(url,filepath,overwrite)

MATCH_COUNT_PER_PAGE = 8
def number_pad_left(seq):
	fmt = u'%03d'
	return fmt % seq

class MatchInfo:

	def __init__(self,spdex,betfair_1x2,betfair_overunder):
		self.spdex = spdex
		self.betfair_1x2 = betfair_1x2
		self.betfair_overunder = betfair_overunder

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
		if self.betfair_1x2:
			betfair_1x2.save_charts()
		if self.betfair_overunder:
			betfair_overunder.save_charts()

class MatchCollectionBydate:

	def __init__(self,id):
		self.id = id
		self.match_list = []

	def add_match(self,match):
		self.match_list.append(match)

	def add_match_list(self,match_list):
		for match in match_list:
			self.add_match(match)

	def match_count(self):
		return len(self.match_list)

def parse_page_core(html,page,mid):
	# parse html (jc or m14)
	datatitle_list = html.xpath('//*[@id="form1"]/div[@class="container"]/div[@class="datatitle"]')
	match_count = len(datatitle_list)
	match_list = []
	for i in xrange(match_count):
		"""
		<div class="datatitle">
			<h3 tid="27428640"> [xxxxxxx] \ aaa VS bbb</h3>
			<span class="matchtime">????:2015/5/2 8:30</span>
			<div class="clear"></div>
		</div>
		"""
		datatitle = datatitle_list[i]

		h3 = datatitle.find('h3')
		span = datatitle.find('span')
		tid = unicode(h3.attrib['tid'])
		vsinfo = h3.text
		start_time = span.text

		seq = MATCH_COUNT_PER_PAGE*(page-1)+(i+1)
		seq = number_pad_left(seq)
		vs = vsinfo.split(u'\\')[1]
		parts = vs.split(u'VS')
		home_name = parts[0].strip()
		away_name = parts[1].strip()
		# 2015/5/2 8:30
		time_fmt = '%Y/%m/%d %H:%M'
		match_time = datetime.strptime(start_time[5:],time_fmt)
		match_id = "{0}{1}".format(mid,seq)

		# 1) SpdexMatchInfo
		spdex_match = SpdexMatchInfo(match_id,home_name,away_name,match_time,tid)

		# 2) BetfairMatchInfo_1X2,BetfairMatchInfo_OverUnder
		href_1x2,href_overunder = parse_viewerqq_page_content(spdex_match.tid)
		betfair_1x2 = parse_betfair_page_1x2(href_1x2,match_id)
		betfair_overunder = parse_betfair_page_overunder(href_overunder,match_id)

		# 3) MatchInfo
		match = MatchInfo(spdex_match,betfair_1x2,betfair_overunder)
		print match.unicode()
		#match.save_charts()
		print "="*100

		# 4 add to match list
		match_list.append(match)
	return match_list

def parse_page_jc(url,jcid,page,viewstate):
	# payload and post
	payload = get_post_payload(jcid,page,viewstate)
	r = requests.post(url,data=payload)
	html = lxml.html.document_fromstring(r.text)
	return parse_page_core(html,page,jcid)

def parse_page_m14(url,m14id):
	# get 
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	page = 1
	return parse_page_core(html,page,m14id)

def parse_viewerqq_page_content(tid):
	url_viewerqq = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id=27428370"
	url_viewerqq_fmt = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id={0}"
	url = url_viewerqq_fmt.format(tid)
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	href_1x2 = html.xpath('/html/body/ul/li[2]/a')[0].attrib['href']
	href_overunder = html.xpath('/html/body/ul/li[3]/a')[0].attrib['href']
	# http://www.spdex.com/Match/View/BetFair/118415106_2740553_0_0
	# http://www.spdex.com/Match/View/BetFair/118415109_47973_0_0
	return href_1x2,href_overunder

def parse_betfair_href(href):
	# http://www.spdex.com/Match/View/BetFair/118415106_2740553_0_0
	parts = href.split('/')
	market_selection = parts[len(parts)-1]
	# 118415106_2740553_0_0
	parts = market_selection.split('_')
	market_id = parts[0]
	selection_id = parts[1]
	return market_id,selection_id

def parse_betfair_page_1x2(href_1x2,match_id):
	market_id,selection_id = parse_betfair_href(href_1x2)
	#url_betfair_1x2 = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118415106&selectionId=2740553"
	#url_betfair_1x2_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
	url = url_betfair_fmt.format(market_id,selection_id)
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	vs_select = html.xpath('//*[@id="myBetsBetView"]')
	if len(vs_select) == 0:
		#print "Betfair market has closed!"
		return None
	vs_select = vs_select[0]
	"""
	<select name="myBetsBetView" id="myBetsBetView" onchange="modifyMyBetsBetView(this)">
		<option value="marketId=118415106&amp;selectionId=2740553" selected="">Arles </option>
		<option value="marketId=118415106&amp;selectionId=269793">Creteil </option>
		<option value="marketId=118415106&amp;selectionId=58805">The Draw </option>
	</select>
	"""
	home_part = vs_select.getchildren()[0]
	home_id = home_part.attrib['value'].split('=')[-1:][0]
	home_eng_name = home_part.text.strip()

	away_part = vs_select.getchildren()[1]
	away_id = away_part.attrib['value'].split('=')[-1:][0]
	away_eng_name = away_part.text.strip()

	draw_part = vs_select.getchildren()[2]
	draw_id = draw_part.attrib['value'].split('=')[-1:][0]

	# object
	betfair_match_info_1x2 = BetfairMatchInfo_1X2(match_id,market_id,home_id,away_id,draw_id,home_eng_name,away_eng_name)
	#print betfair_match_info_1x2.unicode()
	return betfair_match_info_1x2
	
def parse_betfair_page_overunder(href_overunder,match_id):
	market_id,selection_id = parse_betfair_href(href_overunder)
	#url_betfair_overunder = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118415109&selectionId=47973"
	#url_betfair_overunder_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
	url = url_betfair_fmt.format(market_id,selection_id)
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	vs_select = html.xpath('//*[@id="myBetsBetView"]')
	if len(vs_select) == 0:
		#print "Betfair market has closed!"
		return None
	vs_select = vs_select[0]
	"""
	<select name="myBetsBetView" id="myBetsBetView" onchange="modifyMyBetsBetView(this)">
		<option value="marketId=118415109&amp;selectionId=47972">Under 2.5 Goals </option>
		<option value="marketId=118415109&amp;selectionId=47973" selected="">Over 2.5 Goals </option>
	</select>
	"""
	under_part = vs_select.getchildren()[0]
	under_id = under_part.attrib['value'].split('=')[-1:][0]
	under_name = under_part.text.strip()

	over_part = vs_select.getchildren()[1]
	over_id = over_part.attrib['value'].split('=')[-1:][0]
	over_name = over_part.text.strip()

	# object
	betfair_match_info_overunder = BetfairMatchInfo_OverUnder(match_id,market_id,over_id,under_id,over_name,under_name)
	#print betfair_match_info_overunder.unicode()
	return betfair_match_info_overunder
	
def parse_main_jc(url):
	# 1) get params
	page_count,jcid,viewstate = get_params_jc(url)

	# 2) init match collection
	jc = MatchCollectionBydate(jcid)

	# 3) process all pages
	for page in xrange(page_count):
		# [0,1,2,3]
		# 3.1) parse jc page
		match_list = parse_page_jc(url,jcid,page+1,viewstate)

		# 3.2) add to collection
		jc.add_match_list(match_list)
	print jc.match_count()

ROOT_DIR = "charts"

def parse_main_m14(url):
	# 1) get params
	m14id,viewstate = get_params_m14(url)

	# 2) init match collection
	m14 = MatchCollectionBydate(m14id)

	# 3) parse m14 page
	match_list = parse_page_m14(url,m14id)
	
	# 4) add to collection
	m14.add_match_list(match_list)
	print m14.match_count()

def main():
	t1 = time.time()
	#parse_main_jc(url_jc)
	parse_main_m14(url_m14)
	total_time = time.time()-t1
	print "Time used: %f(s)" % total_time

if __name__ == "__main__":
	main()
