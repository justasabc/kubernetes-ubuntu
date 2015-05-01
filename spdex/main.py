#! file-encoding: utf-8
import requests
import lxml.html 
import lxml.etree
from datetime import datetime
import time

url_14_matches = "http://c.spdex.com/spdex500a"
url_jingcai = "http://c.spdex.com/spdex500b"
url_viewerqq_fmt = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id={0}"
url_betfair_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
url_betfair_chart_fmt = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId={0}&selectionId={1}&logarithmic={2}"

"""
url_jingcai = "http://c.spdex.com/spdex500b"
001 27427538
002 27427541

url_viewerqq = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id=27427538"

url_bf_biaopan = "http://www.spdex.com/Match/View/BetFair/118393922_746696_0_0"
url_betfair_biaopan = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118393922&selectionId=746696"

<option value='marketId=118393922&selectionId=746696' selected>Amkar
<option value='marketId=118393922&selectionId=50343'>Dinamo Moscow
<option value='marketId=118393922&selectionId=58805'>The Draw

url_home_log_true = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId=118393922&selectionId=50343&asianLineId=0&logarithmic=true"
url_home_log_false = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId=118393922&selectionId=50343&asianLineId=0&logarithmic=false"

url_bf_daxiaoqiu = "http://www.spdex.com/Match/View/BetFair/118393925_47973_0_0"
url_betfair = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118393925&selectionId=47973"

"""

"""
<table width="100%" border="0" cellpadding="0" cellspacing="0">
	<tbody><tr>
		<td valign="bottom" nowrap="true" style="width:40%;">? 1 ?,? 4 ??</td>
		<td > </td>
	</tr></tbody>
</table>
"""
def get_page_count2(url):
	# //*[@id="AspNetPager1"]/table/tbody/tr/td[1]
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	table = html.xpath('//*[@id="AspNetPager1"]/table')[0]
	#print table.attrib
	#print table.getchildren()
	td = table.find('tr/td')
	#print td.attrib	
	#print td.text

"""
<select name="AspNetPager1_input" id="AspNetPager1_input" onchange="__doPostBack('AspNetPager1','')">
	<option value="1" selected="true">1</option>
	<option value="2">2</option>
	<option value="3">3</option>
	<option value="4">4</option>
</select>

"""

# page_count
# jcid
# VIEWSTATE
def get_jc_params(url):
	#print r.encoding # utf-8
	#print type(r.text) # unicode
	# html element methods
	# http://lxml.de/lxmlhtml.html#html-element-methods
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
	def __init__(self,match_id,home_name,away_name,match_time,spdex_tid):
		self.match_id = match_id
		self.home_name = home_name
		self.away_name = away_name
		self.match_time = match_time
		self.spdex_tid = spdex_tid
		#print type(jcid),type(seq),type(home_name),type(away_name),type(match_time),type(spdex_tid)
		# unicode,unicode,unicode,unicode,datetime.datetime,unicode

	def unicode(self):
		return u"{0},{1} VS {2},{3},{4}".format(self.match_id,self.home_name,self.away_name,self.match_time,self.spdex_tid)

	def __unicode__(self):
		return self.unicode(self)

MATCH_COUNT_PER_PAGE = 8
def seq_pad_left(seq):
	fmt = '%03d'
	return fmt % seq

class MatchCollectionByDate:

	def __init__(self,jcid):
		self.jcid = jcid
		self.match_list = []

	def add_match(self,match):
		self.match_list.append(match)

	def add_match_list(self,match_list):
		for match in match_list:
			self.add_match(match)

	def match_count(self):
		return len(self.match_list)

def parse_jc_page_content(url,jcid,page,viewstate):
	# get html
	payload = get_post_payload(jcid,page,viewstate)
	r = requests.post(url,data=payload)
	html = lxml.html.document_fromstring(r.text)
	# parse html
	datatitle_list = html.xpath('//*[@id="form1"]/div[@class="container"]/div[@class="datatitle"]')
	#match_count = len(datatitle_list)
	match_list = []
	for datatitle in datatitle_list:
		"""
		<div class="datatitle">
			<h3 tid="27428640"> [??20150501??025?] \???? VS ????</h3>
			<span class="matchtime">????:2015/5/2 8:30</span>
			<div class="clear"></div>
		</div>
		"""
		h3 = datatitle.find('h3')
		span = datatitle.find('span')
		tid = unicode(h3.attrib['tid'])
		vsinfo = h3.text
		start_time = span.text

		seq = vsinfo[13:16]
		vs = vsinfo[20:]
		parts = vs.split(u'VS')
		home_name = parts[0].strip()
		away_name = parts[1].strip()
		# 2015/5/2 8:30
		time_fmt = '%Y/%m/%d %H:%M'
		match_time = datetime.strptime(start_time[5:],time_fmt)
		match_id = jcid+seq

		# 1) SpdexMatchInfo
		spdex_match = SpdexMatchInfo(match_id,home_name,away_name,match_time,tid)
		print spdex_match.unicode()

		# 2) BetfairMatchInfo_1X2,BetfairMatchInfo_OverUnder
		betfair_match_info_1x2,betfair_match_info_overunder = parse_betfair_page(tid)
		if betfair_match_info_1x2:
			print betfair_match_info_1x2.unicode()
		if betfair_match_info_overunder:
			print betfair_match_info_overunder.unicode()
			
		match_list.append(spdex_match)
	return match_list

def parse_betfair_page(tid):
	href_1x2,href_overunder = parse_viewerqq_page_content(tid)
	betfair_match_info_1x2 = parse_betfair_page_1x2(href_1x2)
	betfair_match_info_overunder = parse_betfair_page_overunder(href_overunder)
	return betfair_match_info_1x2,betfair_match_info_overunder

class BetfairMatchInfo_1X2:

	def __init__(self,market_id,home_id,away_id,draw_id,home_eng_name,away_eng_name):
		self.market_id = market_id
		self.home_id = home_id
		self.away_id = away_id
		self.draw_id = draw_id
		self.home_eng_name = home_eng_name
		self.away_eng_name = away_eng_name

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

class BetfairMatchInfo_OverUnder:

	def __init__(self,market_id,over_id,under_id,over_name,under_name):
		self.market_id = market_id
		self.over_id = over_id
		self.under_id = under_id
		self.over_name = over_name
		self.under_name = under_name

	def unicode(self):
		return "{0}-{1},{2},{3},{4}".format(self.over_name,self.under_name,self.market_id,self.over_id,self.under_id)

	def get_over_chart_url(self,log):
		url = url_betfair_chart_fmt.format(self.market_id,self.over_id,log)
		return url
	def get_under_chart_url(self,log):
		url = url_betfair_chart_fmt.format(self.market_id,self.under_id,log)
		return url

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

def parse_betfair_page_1x2(href_1x2):
	market_id,selection_id = parse_betfair_href(href_1x2)
	#url_betfair_1x2 = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118415106&selectionId=2740553"
	#url_betfair_1x2_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
	url = url_betfair_fmt.format(market_id,selection_id)
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	vs_select = html.xpath('//*[@id="myBetsBetView"]')
	if len(vs_select) == 0:
		print "Betfair market has closed!"
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
	betfair_match_info_1x2 = BetfairMatchInfo_1X2(market_id,home_id,away_id,draw_id,home_eng_name,away_eng_name)
	#print betfair_match_info_1x2.unicode()
	return betfair_match_info_1x2
	
def parse_betfair_page_overunder(href_overunder):
	market_id,selection_id = parse_betfair_href(href_overunder)
	#url_betfair_overunder = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118415109&selectionId=47973"
	#url_betfair_overunder_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
	url = url_betfair_fmt.format(market_id,selection_id)
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)
	vs_select = html.xpath('//*[@id="myBetsBetView"]')
	if len(vs_select) == 0:
		print "Betfair market has closed!"
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
	betfair_match_info_overunder = BetfairMatchInfo_OverUnder(market_id,over_id,under_id,over_name,under_name)
	#print betfair_match_info_overunder.unicode()
	return betfair_match_info_overunder
	

def get_all_tids(url):
	# 1) get params
	page_count,jcid,viewstate = get_jc_params(url)
	match_collection = MatchCollectionByDate(jcid)
	# 2) process all pages
	for page in xrange(1,page_count+1):
		match_list = parse_jc_page_content(url,jcid,page,viewstate)
		match_collection.add_match_list(match_list)
	print match_collection.match_count()

def main():
	get_all_tids(url_jingcai)

if __name__ == "__main__":
	main()
