# -*- coding:utf-8 -*-
import requests
import lxml.html 
from datetime import datetime,timedelta
import time
from threading import Timer 

from utility import *
from setting import *
from spdex.spdex_setting import *
from spdex.spdex_match import *

# GLOBAL
# JC M14
def get_id_list_viewstate(match_type):
	url = GSPDEX[match_type].get("URL")
	ui_select_id = GSPDEX[match_type].get("UI_SELECT_ID")
	r = requests.get(url)
	html = lxml.html.document_fromstring(r.text)

	# 1) id list
	#path = '//*[@id="DropJcId"]'
	path = '//*[@id="{0}"]'.format(ui_select_id)
	id_select = html.xpath(path)
	id_list = []
	if len(id_select) == 0:
		print "Empyt id list!"
		return id_list,None
	id_select = id_select[0]
	for c in id_select.getchildren():
		id = c.text.strip()
		id_list.append(id)

	# 2) viewstate
	path = '//*[@id="__VIEWSTATE"]'
	viewstate_input = html.xpath(path)[0]
	viewstate = viewstate_input.attrib['value']
	return id_list,viewstate

def get_page_count_jc(url,sid,viewstate):
	payload = get_post_payload_jc(sid,1,viewstate)
	r = requests.post(url,data=payload)
	html = lxml.html.document_fromstring(r.text)
	path = '//*[@id="AspNetPager1_input"]'
	# page_count
	page_select = html.xpath(path)[0]
	page_options = page_select.getchildren()
	page_count = len(page_options)
	return page_count

def get_page_count_m14(url,sid,viewstate):
	return 1

def get_page_count(match_type,sid,viewstate):
	url = GSPDEX[match_type].get("URL")
	if match_type == MATCH_TYPE_JC:
		return get_page_count_jc(url,sid,viewstate)
	elif match_type == MATCH_TYPE_M14:
		return get_page_count_m14(url,sid,viewstate)

"""
__EVENTTARGET:AspNetPager1
__EVENTARGUMENT:
__LASTFOCUS:
__VIEWSTATE: xxx
DropJcId:20150430
AspNetPager1_input:2
"""
def get_post_payload_jc(sid,page,viewstate):
	payload = {}
	payload['__EVENTTARGET'] = 'AspNetPager1'
	payload['__EVENTARGUMENT'] = None
	payload['__LASTFOCUS'] = None
	payload['__VIEWSTATE'] = viewstate
	payload['DropJcId'] = sid
	payload['AspNetPager1_input'] = page
	return payload

"""
_EVENTTARGET:DropLotteryId
__EVENTARGUMENT:
__LASTFOCUS:
__VIEWSTATE: xxx
DropLotteryId:15068
"""
def get_post_payload_m14(sid,page,viewstate):
	payload = {}
	payload['__EVENTTARGET'] = 'DropLotteryId'
	payload['__EVENTARGUMENT'] = None
	payload['__LASTFOCUS'] = None
	payload['__VIEWSTATE'] = viewstate
	payload['DropLotteryId'] = sid
	return payload

def get_post_payload(match_type,sid,page,viewstate):
	if match_type == MATCH_TYPE_JC:
		return get_post_payload_jc(sid,page,viewstate)
	elif match_type == MATCH_TYPE_M14:
		return get_post_payload_m14(sid,page,viewstate)

# sid 20150501
# seq 001
# mid 20150501001
def parse_page_core(match_type,sid,page,viewstate):
	# get html
	url = GSPDEX[match_type].get("URL")
	per_page = GSPDEX[match_type].get("PER_PAGE")
	payload = get_post_payload(match_type,sid,page,viewstate)
	r = requests.post(url,data=payload)
	html = lxml.html.document_fromstring(r.text)

	# parse html (jc or m14)
	path = '//*[@id="form1"]/div[@class="container"]/div[@class="datatitle"]'
	datatitle_list = html.xpath(path)
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

		seq = per_page*(page-1)+(i+1)
		seq = pad_seq(seq)
		vs = vsinfo.split(u'\\')[1]
		parts = vs.split(u'VS')
		home_name = parts[0].strip()
		away_name = parts[1].strip()
		# 2015/5/2 8:30
		time_fmt = '%Y/%m/%d %H:%M'
		match_time = datetime.strptime(start_time[5:],time_fmt)
		match_id = "{0}{1}".format(sid,seq)

		# 1) SpdexMatchInfo
		spdex_match = SpdexMatchInfo(match_id,home_name,away_name,match_time,tid)

		# 2) BetfairMatchInfo_1X2,BetfairMatchInfo_OverUnder
		href_1x2,href_overunder = parse_viewerqq_page_content(spdex_match.tid)
		betfair_1x2 = parse_betfair_page_1x2(href_1x2,match_id)
		betfair_overunder = parse_betfair_page_overunder(href_overunder,match_id)

		# 3) MatchInfo
		match = MatchInfo(match_type,sid,spdex_match,betfair_1x2,betfair_overunder)
		print "="*100

		# 4 add to match list
		match_list.append(match)
	return match_list

def parse_viewerqq_page_content(tid):
	#url_viewerqq = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id=27428370"
	#url_viewerqq_fmt = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id={0}"
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
	return betfair_match_info_overunder

def parse_main(match_type):
	# get id list
	id_list,viewstate = get_id_list_viewstate(match_type)
	print id_list

	# process the first sid only
	if len(id_list) :
		id_list  = id_list[:1]
	if match_type == MATCH_TYPE_JC:
		sid = get_today_sid_jc()
		id_list = [sid]
	
	print id_list
	# process all id
	for sid in id_list:
		print "*"*100
		print "Processing {0}...".format(sid)
		print "*"*100
		# 1) init match collection
		mc = MatchCollectionBydate(sid)

		# 2) get page count for sid
		page_count = get_page_count(match_type,sid,viewstate)

		# 3) process all pages
		#page_count = 4
		for page in xrange(page_count):
			# [0,1,2,3]
			# 3.1) parse jc page
			match_list = parse_page_core(match_type,sid,page+1,viewstate)

			# 3.2) add to collection
			mc.add_match_list(match_list)
		print mc.match_count()

def spdex_main():
	t1 = time.time()
	parse_main(MATCH_TYPE_JC)
	parse_main(MATCH_TYPE_M14)
	total_time = time.time()-t1
	print "Time used: %f(s)" % total_time
